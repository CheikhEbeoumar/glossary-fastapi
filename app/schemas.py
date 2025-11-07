from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class RenderingType(str, Enum):
    SSR = "SSR"
    SSG = "SSG"
    CSR = "CSR"
    ISR = "ISR"
    DSR = "DSR"

class TermBase(BaseModel):
    name: str
    description: str
    rendering_type: RenderingType
    frameworks: List[str]  # e.g., ["Next.js", "Nuxt.js", "Gatsby"]
    use_cases: List[str]   # e.g., ["E-commerce", "Blog", "Dashboard"]
    advantages: List[str]
    disadvantages: List[str]

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rendering_type: Optional[RenderingType] = None
    frameworks: Optional[List[str]] = None
    use_cases: Optional[List[str]] = None
    advantages: Optional[List[str]] = None
    disadvantages: Optional[List[str]] = None

class Term(TermBase):
    id: int

    class Config:
        from_attributes = True
        
class TermRelationship(BaseModel):
    source_term_id: int
    target_term_id: int
    relationship_type: str  # e.g., "similar_to", "alternative_to", "enhances"

class TermWithRelationships(Term):
    relationships: List[TermRelationship]