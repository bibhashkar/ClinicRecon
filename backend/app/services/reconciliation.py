from app.models.patient import ReconcileRequest, ReconcileResponse
from app.llm.client import call_llm
from app.llm.prompts import RECONCILE_SYSTEM_PROMPT, RECONCILE_USER_TEMPLATE
from app.utils.clinical_rules import calculate_recency_score, adjust_for_egfr
import json

async def reconcile_medication(request: ReconcileRequest) -> ReconcileResponse:
    # Rule-based pre-processing
    best_source = max(request.sources, key=lambda s: calculate_recency_score(s.dict()) * (1 if s.source_reliability == "high" else 0.7))
    candidate = adjust_for_egfr(best_source.medication, request.patient_context.recent_labs.get("eGFR", 999))

    # LLM for reasoning + safety
    user_prompt = RECONCILE_USER_TEMPLATE.format(
        patient_context=json.dumps(request.patient_context.dict()),
        sources=json.dumps([s.dict() for s in request.sources])
    )
    llm_raw = await call_llm(RECONCILE_SYSTEM_PROMPT, user_prompt)
    llm_data = json.loads(llm_raw)

    return ReconcileResponse(
        reconciled_medication=llm_data.get("reconciled_medication", candidate),
        confidence_score=llm_data.get("confidence_score", 0.75),
        reasoning=llm_data.get("reasoning", ""),
        recommended_actions=llm_data.get("recommended_actions", []),
        clinical_safety_check=llm_data.get("clinical_safety_check", "PASSED")
    )