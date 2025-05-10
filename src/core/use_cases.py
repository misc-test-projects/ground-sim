from __future__ import annotations
from datetime import timedelta
from typing import Tuple, List
from .models import Plan


class ValidationError(Exception):
    pass


def validate_plan(plan: Plan) -> None:
    # Check time window length (> 0 and <= 8 hours for demo purposes)
    delta = plan.window_end - plan.window_start
    if delta <= timedelta(0) or delta > timedelta(hours=8):
        raise ValidationError("Invalid time window length")

    # Resource sanity
    if not plan.resources:
        raise ValidationError("At least one resource required")

    # Constraint checks (example: min separation must be non-negative)
    if "min_separation_minutes" in plan.constraints and plan.constraints["min_separation_minutes"] < 0:
        raise ValidationError("min_separation_minutes must be >= 0")


def verify_plan(plan: Plan) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    # Example verification: ensure capacity sum >= required minimum (demo logic)
    capacity_sum = sum(r.capacity for r in plan.resources)
    if capacity_sum < 2:
        reasons.append("Insufficient aggregate capacity (<2)")
    # Example: min separation must be <= window length in minutes
    if "min_separation_minutes" in plan.constraints:
        mins = plan.constraints["min_separation_minutes"]
        length_mins = int((plan.window_end - plan.window_start).total_seconds() / 60)
        if mins > length_mins:
            reasons.append("min_separation_minutes exceeds window length")
    return (len(reasons) == 0, reasons)
