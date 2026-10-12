"""Pure risk scoring logic for MonsoonReady AI.

This module provides a dependency‑free function `compute_priority` that can be used
both by the FastAPI backend and by unit tests without requiring FastAPI, SQLModel,
or any third‑party libraries.
"""

from typing import Dict, Any


def compute_priority(report: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate a deterministic priority score.

    Parameters
    ----------
    report: dict
        Expected keys ``severity`` (int), ``water_depth_cm`` (optional int or float),
        and ``critical_infra`` (bool). Missing optional fields default to ``0`` or
        ``False``.

    Returns
    -------
    dict
        Contains ``score`` (float), ``category`` ("HIGH", "MEDIUM", "LOW"), and an
        ``explanation`` string describing the contribution of each factor.
    """
    severity = report.get("severity", 0) if isinstance(report, dict) else getattr(report, "severity", 0)
    water_depth_cm = report.get("water_depth_cm", 0) if isinstance(report, dict) else getattr(report, "water_depth_cm", 0) or 0
    critical_infra = report.get("critical_infra", False) if isinstance(report, dict) else getattr(report, "critical_infra", False)

    # Base weight by severity (1-5) – each point contributes 2.0
    severity_weight = severity * 2.0
    # Water depth contributes 0.1 per centimetre
    depth_weight = water_depth_cm * 0.1
    # Critical infrastructure adds a flat 5.0 if present
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
