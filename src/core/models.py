from __future__ import annotations
from pydantic import BaseModel, Field, AwareDatetime, validator
from typing import List, Dict


class Resource(BaseModel):
    name: str
    capacity: int = Field(ge=1)


class Plan(BaseModel):
    id: str
    version: int = Field(ge=1)
    window_start: AwareDatetime
    window_end: AwareDatetime
    resources: List[Resource]
    constraints: Dict[str, int] = {}

    @validator("window_end")
    def validate_window(cls, v, values):
        ws = values.get("window_start")
        if ws and v <= ws:
            raise ValueError("window_end must be after window_start")
        return v
