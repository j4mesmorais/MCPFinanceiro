from fastapi import FastAPI, Depends, HTTPException
from datetime import timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_session, Base, engine
from .models import Person
from services.people import create_person, get_person, list_people, update_person, delete_person
from .mcp import router as mcp_router
from .auth import create_access_token, verify_token, security


# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(mcp_router, dependencies=[Depends(verify_token)])


class PersonCreate(BaseModel):
    name: str
    email: str


class PersonOut(PersonCreate):
    id: int

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/token", response_model=TokenResponse)
def issue_token():
    """Issue a simple JWT token for demonstration purposes."""
    token = create_access_token({"sub": "demo"}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}


@app.post("/people", response_model=PersonOut)
def create(
    person: PersonCreate,
    db: Session = Depends(get_session),
    _: dict = Depends(verify_token),
):
    return create_person(db, name=person.name, email=person.email)


@app.get("/people", response_model=list[PersonOut])
def read_all(db: Session = Depends(get_session), _: dict = Depends(verify_token)):
    return list_people(db)


@app.get("/people/{person_id}", response_model=PersonOut)
def read_one(
    person_id: int,
    db: Session = Depends(get_session),
    _: dict = Depends(verify_token),
):
    person = get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.put("/people/{person_id}", response_model=PersonOut)
def update(
    person_id: int,
    person: PersonCreate,
    db: Session = Depends(get_session),
    _: dict = Depends(verify_token),
):
    person_obj = update_person(db, person_id, name=person.name, email=person.email)
    return person_obj


@app.delete("/people/{person_id}", status_code=204)
def delete(
    person_id: int,
    db: Session = Depends(get_session),
    _: dict = Depends(verify_token),
):
    delete_person(db, person_id)
    return None


__all__ = ["app"]
