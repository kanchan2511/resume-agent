from pydantic import BaseModel, Field
from typing import List

class ResumeRequest(BaseModel):
    text: str

class ResumeAnalysis(BaseModel):
    strengths: List[str] = Field(description="Key hightlights of the resume")
    weaknesses: List[str]
    missing_skills: List[str]
    suggestions: List[str]
