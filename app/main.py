from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Glossary API",
    description="A simple glossary service for managing terms and definitions",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Glossary API"}

@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_name(db, name=term.name)
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    return crud.create_term(db=db, term=term)

@app.get("/terms/", response_model=List[schemas.Term])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms

@app.get("/terms/{term_id}", response_model=schemas.Term)
def read_term(term_id: int, db: Session = Depends(get_db)):
    db_term = crud.get_term(db, term_id=term_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.put("/terms/{term_id}", response_model=schemas.Term)
def update_term(term_id: int, term: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = crud.update_term(db, term_id=term_id, term=term)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.delete("/terms/{term_id}")
def delete_term(term_id: int, db: Session = Depends(get_db)):
    success = crud.delete_term(db, term_id=term_id)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"message": "Term deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)