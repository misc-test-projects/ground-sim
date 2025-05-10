from src.core.models import Plan, Resource
import pytest
from datetime import datetime, timezone, timedelta

def test_plan_window_validation():
    ws = datetime.now(timezone.utc)
    we = ws + timedelta(hours=1)
    p = Plan(id="p1", version=1, window_start=ws, window_end=we, resources=[Resource(name="r", capacity=1)])
    assert p.window_end > p.window_start

def test_plan_invalid_window():
    ws = datetime.now(timezone.utc)
    with pytest.raises(Exception):
        Plan(id="p1", version=1, window_start=ws, window_end=ws, resources=[Resource(name="r", capacity=1)])
