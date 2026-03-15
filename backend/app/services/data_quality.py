from app.models.patient import DataQualityRecord, DataQualityResponse
from app.llm.client import call_llm
from app.llm.prompts import DATA_QUALITY_SYSTEM_PROMPT, DATA_QUALITY_USER_TEMPLATE
from functools import lru_cache
import json
from datetime import datetime, timedelta

async def validate_data_quality(record: DataQualityRecord) -> DataQualityResponse:
    # Rule-based pre-processing
    completeness_score = calculate_completeness(record)
    accuracy_score = calculate_accuracy(record)
    timeliness_score = calculate_timeliness(record)
    plausibility_score = calculate_clinical_plausibility(record)

    issues = []
    issues.extend(check_completeness_issues(record))
    issues.extend(check_accuracy_issues(record))
    issues.extend(check_timeliness_issues(record))
    issues.extend(check_plausibility_issues(record))

    # LLM for advanced reasoning + safety
    user_prompt = DATA_QUALITY_USER_TEMPLATE.format(
        record=json.dumps(record.dict())
    )
    try:
        llm_raw = await call_llm(DATA_QUALITY_SYSTEM_PROMPT, user_prompt)
        llm_data = json.loads(llm_raw)
        additional_issues = llm_data.get("additional_issues", [])
        issues.extend(additional_issues)
    except Exception as e:
        print(f"LLM call failed for data quality: {e}. Using rule-based only.")

    overall_score = int((completeness_score + accuracy_score + timeliness_score + plausibility_score) / 4)

    return DataQualityResponse(
        overall_score=overall_score,
        breakdown={
            "completeness": completeness_score,
            "accuracy": accuracy_score,
            "timeliness": timeliness_score,
            "clinical_plausibility": plausibility_score
        },
        issues_detected=issues
    )

def calculate_completeness(record: DataQualityRecord) -> int:
    total_fields = 6  # demographics, medications, allergies, conditions, vital_signs, last_updated
    filled = sum([
        bool(record.demographics),
        bool(record.medications),
        bool(record.allergies),
        bool(record.conditions),
        bool(record.vital_signs),
        bool(record.last_updated)
    ])
    return int((filled / total_fields) * 100)

def calculate_accuracy(record: DataQualityRecord) -> int:
    # Basic checks: no empty strings, valid formats
    score = 100
    if any(not med.strip() for med in record.medications):
        score -= 20
    if any(not cond.strip() for cond in record.conditions):
        score -= 20
    # Add more accuracy checks as needed
    return max(0, score)

def calculate_timeliness(record: DataQualityRecord) -> int:
    try:
        last_updated = datetime.fromisoformat(record.last_updated.replace('Z', '+00:00'))
        now = datetime.now(last_updated.tzinfo)
        days_old = (now - last_updated).days
        if days_old <= 30:
            return 100
        elif days_old <= 90:
            return 75
        elif days_old <= 365:
            return 50
        else:
            return 25
    except:
        return 0

def calculate_clinical_plausibility(record: DataQualityRecord) -> int:
    score = 100
    # Check for impossible values
    if 'systolic_bp' in record.vital_signs and 'diastolic_bp' in record.vital_signs:
        sys = record.vital_signs['systolic_bp']
        dia = record.vital_signs['diastolic_bp']
        if sys <= dia or sys > 300 or dia < 40:
            score -= 30
    # Check age vs conditions
    age = record.demographics.get('age', 0)
    if age < 18 and 'diabetes' in [c.lower() for c in record.conditions]:
        score -= 20
    return max(0, score)

def check_completeness_issues(record: DataQualityRecord) -> list:
    issues = []
    if not record.demographics:
        issues.append({"field": "demographics", "issue": "Missing demographics", "severity": "high"})
    if not record.medications:
        issues.append({"field": "medications", "issue": "No medications listed", "severity": "medium"})
    if not record.allergies:
        issues.append({"field": "allergies", "issue": "Allergies not documented", "severity": "medium"})
    if not record.conditions:
        issues.append({"field": "conditions", "issue": "No conditions recorded", "severity": "high"})
    if not record.vital_signs:
        issues.append({"field": "vital_signs", "issue": "Missing vital signs", "severity": "medium"})
    if not record.last_updated:
        issues.append({"field": "last_updated", "issue": "No update timestamp", "severity": "low"})
    return issues

def check_accuracy_issues(record: DataQualityRecord) -> list:
    issues = []
    for med in record.medications:
        if not med.strip():
            issues.append({"field": "medications", "issue": "Empty medication entry", "severity": "medium"})
    for cond in record.conditions:
        if not cond.strip():
            issues.append({"field": "conditions", "issue": "Empty condition entry", "severity": "medium"})
    return issues

def check_timeliness_issues(record: DataQualityRecord) -> list:
    issues = []
    try:
        last_updated = datetime.fromisoformat(record.last_updated.replace('Z', '+00:00'))
        now = datetime.now(last_updated.tzinfo)
        days_old = (now - last_updated).days
        if days_old > 365:
            issues.append({"field": "last_updated", "issue": f"Record is {days_old} days old", "severity": "high"})
        elif days_old > 90:
            issues.append({"field": "last_updated", "issue": f"Record is {days_old} days old", "severity": "medium"})
    except:
        issues.append({"field": "last_updated", "issue": "Invalid date format", "severity": "high"})
    return issues

def check_plausibility_issues(record: DataQualityRecord) -> list:
    issues = []
    if 'systolic_bp' in record.vital_signs and 'diastolic_bp' in record.vital_signs:
        sys = record.vital_signs['systolic_bp']
        dia = record.vital_signs['diastolic_bp']
        if sys <= dia:
            issues.append({"field": "vital_signs", "issue": "Systolic BP <= Diastolic BP", "severity": "high"})
        if sys > 300 or dia < 40:
            issues.append({"field": "vital_signs", "issue": "Impossible BP values", "severity": "high"})
    age = record.demographics.get('age', 0)
    if age < 18 and any('diabetes' in c.lower() for c in record.conditions):
        issues.append({"field": "conditions", "issue": "Diabetes in pediatric patient", "severity": "high"})
    return issues