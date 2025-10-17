from pydantic import BaseModel
from typing import Optional

class TermBase(BaseModel):
    name: str
    description: str

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Term(TermBase):
    id: int

    class Config:
        from_attributes = True