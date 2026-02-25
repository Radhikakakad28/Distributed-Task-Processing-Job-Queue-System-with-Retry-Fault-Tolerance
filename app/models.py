from pydantic import BaseModel, Field
from typing import Dict, Any


class Job(BaseModel):
    task_id: str
    payload: Dict[str, Any]

    priority: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Priority level (1 = highest, 5 = lowest)"
    )

    retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts allowed"
    )