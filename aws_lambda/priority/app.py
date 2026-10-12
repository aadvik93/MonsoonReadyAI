import json
from typing import Any, Dict

# Re‑use the same pure‑Python scoring logic (copied from backend/app/risk.py) to keep the Lambda self‑contained.

def compute_priority(report: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate a deterministic priority score.

    Parameters
    ----------
    report: dict
        Expected keys ``severity`` (int), ``water_depth_cm`` (optional int/float),
        and ``critical_infra`` (bool). Missing optional fields default to ``0`` or
        ``False``.

    Returns
    -------
    dict
        Contains ``score`` (float), ``category`` ("HIGH", "MEDIUM", "LOW"), and an
        ``explanation`` string.
    """
    severity = report.get("severity", 0)
    water_depth_cm = report.get("water_depth_cm", 0) or 0
    critical_infra = report.get("critical_infra", False)

    severity_weight = severity * 2.0
    depth_weight = water_depth_cm * 0.1
    infra_weight = 5.0 if critical_infra else 0.0

    score = severity_weight + depth_weight + infra_weight

    if score >= 15:
        category = "HIGH"
    elif score >= 8:
        category = "MEDIUM"
    else:
        category = "LOW"

    explanation = (
        f"Severity ({severity}) contributes {severity_weight}, "
        f"water depth ({water_depth_cm} cm) contributes {depth_weight:.1f}, "
        f"critical infra ({critical_infra}) contributes {infra_weight}. "
        f"Total score {score:.1f} => {category} priority."
    )
    return {"score": score, "category": category, "explanation": explanation}


def lambda_handler(event, context):
    """AWS Lambda entry point.

    Expected ``event`` shape (JSON) – a dict with the same fields used by the
    FastAPI ``Report`` model, e.g.:
    {
        "severity": 3,
        "water_depth_cm": 12,
        "critical_infra": true
    }
    The function returns the same structure as ``compute_priority``.
    """
    # The event may be a JSON string if invoked via API Gateway; handle both.
    if isinstance(event, str):
        try:
            payload = json.loads(event)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON payload"}
    else:
        payload = event
    result = compute_priority(payload)
    return result
