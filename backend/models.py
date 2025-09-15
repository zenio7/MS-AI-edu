from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ConceptAnalysisRequest(BaseModel):
    concepts: List[str] = Field(..., min_items=1, max_items=5, description="1-5 concepts to analyze")

    @validator('concepts')
    def validate_concepts(cls, v):
        if len(v) < 1:
            raise ValueError('At least 1 concept is required')
        if len(v) > 5:
            raise ValueError('Maximum 5 concepts are allowed')

        # Check for empty or duplicate concepts
        clean_concepts = [concept.strip() for concept in v if concept.strip()]
        if len(clean_concepts) != len(v):
            raise ValueError('All concepts must be non-empty')

        if len(set(c.lower() for c in clean_concepts)) != len(clean_concepts):
            raise ValueError('All concepts must be unique')

        return clean_concepts

class ConceptData(BaseModel):
    name: str
    unique: List[str] = Field(..., min_items=5, max_items=12, description="5-12 unique concepts for this concept")

class ConceptAnalysisResponse(BaseModel):
    concepts: List[ConceptData] = Field(..., description="Analysis results for each concept")
    shared_concepts: List[str] = Field(default=[], description="Concepts shared among input concepts (empty for single concept)")
    similarity_matrix: Optional[dict] = Field(None, description="Pairwise similarity information")
    analysis_id: Optional[str] = Field(None, description="LangSmith trace ID for debugging")
    analysis_type: str = Field(..., description="single or comparison analysis")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None