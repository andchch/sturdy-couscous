from typing import List, Dict
from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    user: Dict
    compatibility_score: float
    matching_factors: List[str] 