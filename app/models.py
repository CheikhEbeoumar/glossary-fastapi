from sqlalchemy import Column, Integer, String, Text, JSON
from .database import Base

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    rendering_type = Column(String(20), nullable=False)  # SSR, SSG, CSR
    frameworks = Column(JSON, nullable=False)  # List of frameworks as JSON
    use_cases = Column(JSON, nullable=False)   # List of use cases
    advantages = Column(JSON, nullable=False)  # List of advantages
    disadvantages = Column(JSON, nullable=False) # List of disadvantages