from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClaimCreate(BaseModel):
    policy_number: str
    amount: float

class ClaimResponse(BaseModel):
    id: int
    policy_number: str
    amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
