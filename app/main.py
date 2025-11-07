from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from . import crud, models, schemas
from .database import SessionLocal, engine
from .initial_data import get_initial_terms

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Web Rendering Methods Glossary API",
    description="A specialized glossary for SSR, SSG, and CSR rendering methods research",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize with sample data
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Check if terms already exist
        existing_terms = db.query(models.Term).count()
        if existing_terms == 0:
            # Add initial terms for the thesis research
            initial_terms = get_initial_terms()
            for term_data in initial_terms:
                db_term = models.Term(
                    name=term_data["name"],
                    description=term_data["description"],
                    rendering_type=term_data["rendering_type"],
                    frameworks=term_data["frameworks"],
                    use_cases=term_data["use_cases"],
                    advantages=term_data["advantages"],
                    disadvantages=term_data["disadvantages"]
                )
                db.add(db_term)
            db.commit()
            print("Initial terms added to database")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Web Rendering Methods Glossary API",
        "description": "Research on SSR, SSG and CSR rendering methods in web frameworks",
        "endpoints": {
            "docs": "/docs",
            "all_terms": "/terms/",
            "search_by_type": "/terms/type/{rendering_type}",
            "search_by_framework": "/terms/framework/{framework_name}"
        }
    }

@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    """
    Create a new term with all rendering method details
    """
    db_term = crud.get_term_by_name(db, name=term.name)
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    return crud.create_term(db=db, term=term)

@app.get("/terms/", response_model=List[schemas.Term])
def read_terms(
    skip: int = 0, 
    limit: int = 100,
    rendering_type: Optional[schemas.RenderingType] = None,
    db: Session = Depends(get_db)
):
    """
    Get all terms with optional filtering by rendering type
    """
    terms = crud.get_terms(db, skip=skip, limit=limit, rendering_type=rendering_type)
    return terms

@app.get("/terms/{term_id}", response_model=schemas.Term)
def read_term(term_id: int, db: Session = Depends(get_db)):
    """
    Get a specific term by ID
    """
    db_term = crud.get_term(db, term_id=term_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.get("/terms/type/{rendering_type}", response_model=List[schemas.Term])
def read_terms_by_type(rendering_type: schemas.RenderingType, db: Session = Depends(get_db)):
    """
    Get all terms of a specific rendering type (SSR, SSG, CSR, etc.)
    """
    terms = crud.get_terms_by_rendering_type(db, rendering_type=rendering_type)
    if not terms:
        raise HTTPException(status_code=404, detail=f"No terms found for rendering type: {rendering_type}")
    return terms

@app.get("/terms/framework/{framework_name}", response_model=List[schemas.Term])
def read_terms_by_framework(framework_name: str, db: Session = Depends(get_db)):
    """
    Get all terms that support a specific framework
    """
    terms = crud.get_terms_by_framework(db, framework_name=framework_name)
    if not terms:
        raise HTTPException(status_code=404, detail=f"No terms found for framework: {framework_name}")
    return terms

@app.put("/terms/{term_id}", response_model=schemas.Term)
def update_term(term_id: int, term: schemas.TermUpdate, db: Session = Depends(get_db)):
    """
    Update an existing term - all fields are optional
    """
    db_term = crud.update_term(db, term_id=term_id, term=term)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.delete("/terms/{term_id}")
def delete_term(term_id: int, db: Session = Depends(get_db)):
    """
    Delete a term from the glossary
    """
    success = crud.delete_term(db, term_id=term_id)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"message": "Term deleted successfully"}

@app.get("/stats/")
def get_glossary_stats(db: Session = Depends(get_db)):
    """
    Get statistics about the glossary terms
    """
    stats = crud.get_glossary_stats(db)
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)