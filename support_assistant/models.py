from pydantic import BaseModel, Field
from typing import List


# ==============================
# Request Model
# ==============================

class QueryRequest(BaseModel):
    query: str = Field(..., description="User question")


# ==============================
# Response Model
# ==============================

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float