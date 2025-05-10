from datetime import datetime, timedelta, timezone
from src.core.models import Plan, Resource
from src.core.use_cases import validate_plan, verify_plan, ValidationError

def test_validate_plan_ok():
    ws = datetime.now(timezone.utc)
    plan = Plan(
        id="ok", version=1,
        window_start=ws, window_end=ws + timedelta(hours=1),
        resources=[Resource(name="radar", capacity=2)],
        constraints={"min_separation_minutes": 5},
    )
    validate_plan(plan)

def test_verify_plan_reject_for_capacity():
    ws = datetime.now(timezone.utc)
    plan = Plan(
        id="lowcap", version=1,
        window_start=ws, window_end=ws + timedelta(hours=1),
        resources=[Resource(name="radar", capacity=1)],
        constraints={},
    )
    ok, reasons = verify_plan(plan)
    assert not ok
    assert any("Insufficient" in r for r in reasons)
