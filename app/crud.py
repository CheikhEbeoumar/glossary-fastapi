from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from typing import List, Optional

def get_term(db: Session, term_id: int):
    return db.query(models.Term).filter(models.Term.id == term_id).first()

def get_term_by_name(db: Session, name: str):
    return db.query(models.Term).filter(models.Term.name == name).first()

def get_terms(db: Session, skip: int = 0, limit: int = 100, rendering_type: Optional[str] = None):
    query = db.query(models.Term)
    if rendering_type:
        query = query.filter(models.Term.rendering_type == rendering_type)
    return query.offset(skip).limit(limit).all()

def get_terms_by_rendering_type(db: Session, rendering_type: str):
    return db.query(models.Term).filter(models.Term.rendering_type == rendering_type).all()

def get_terms_by_framework(db: Session, framework_name: str):
    # Search for framework in the JSON array field
    return db.query(models.Term).filter(
        models.Term.frameworks.contains([framework_name])
    ).all()

def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(
        name=term.name,
        description=term.description,
        rendering_type=term.rendering_type,
        frameworks=term.frameworks,
        use_cases=term.use_cases,
        advantages=term.advantages,
        disadvantages=term.disadvantages
    )
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def update_term(db: Session, term_id: int, term: schemas.TermUpdate):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term:
        update_data = term.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_term, field, value)
        db.commit()
        db.refresh(db_term)
    return db_term

def delete_term(db: Session, term_id: int):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term:
        db.delete(db_term)
        db.commit()
        return True
    return False

def get_glossary_stats(db: Session):
    total_terms = db.query(models.Term).count()
    
    # Count by rendering type
    rendering_stats = {}
    for rendering_type in ['SSR', 'SSG', 'CSR', 'ISR', 'DSR']:
        count = db.query(models.Term).filter(models.Term.rendering_type == rendering_type).count()
        rendering_stats[rendering_type] = count
    
    # Get all unique frameworks
    all_frameworks = set()
    terms = db.query(models.Term).all()
    for term in terms:
        all_frameworks.update(term.frameworks)
    
    return {
        "total_terms": total_terms,
        "rendering_type_distribution": rendering_stats,
        "unique_frameworks": list(all_frameworks),
        "total_frameworks_covered": len(all_frameworks)
    }