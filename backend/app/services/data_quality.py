# (Similar structure – abbreviated for space; full version identical pattern)
from app.utils.clinical_rules import is_plausible_bp


async def validate_data_quality(record: dict):
    # Rule checks first (BP, age, missing allergies, old data)
    issues = []
    if "vital_signs" in record and not is_plausible_bp(record["vital_signs"].get("blood_pressure")):
        issues.append({"field": "vital_signs.blood_pressure", "issue": "Physiologically implausible", "severity": "high"})
    # ... add more rules
    # Then LLM for final scoring
    # Return DataQualityResponse