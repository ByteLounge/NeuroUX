from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Recommendation(BaseModel):
    text: str
    severity: str

class AnalysisResult(BaseModel):
    id: str # Temporary UUID for session
    created_at: datetime
    original_image_path: str
    cfi_score: float
    vcs_score: float
    ifs_score: float
    ddp_score: float
    ux_intelligence_score: float
    saliency_heatmap_path: str
    recommendations: List[Recommendation]
