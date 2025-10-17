from sqlalchemy.orm import Session
from . import models, schemas

def get_term(db: Session, term_id: int):
    return db.query(models.Term).filter(models.Term.id == term_id).first()

def get_term_by_name(db: Session, name: str):
    return db.query(models.Term).filter(models.Term.name == name).first()

def get_terms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Term).offset(skip).limit(limit).all()

def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(name=term.name, description=term.description)
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