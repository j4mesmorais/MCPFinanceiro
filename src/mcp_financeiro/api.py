from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_session, Base, engine
from .models import Person
from services.people import create_person, get_person, list_people, update_person, delete_person


# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


class PersonCreate(BaseModel):
    name: str
    email: str


class PersonOut(PersonCreate):
    id: int

    class Config:
        orm_mode = True


@app.post("/people", response_model=PersonOut)
def create(person: PersonCreate, db: Session = Depends(get_session)):
    return create_person(db, name=person.name, email=person.email)


@app.get("/people", response_model=list[PersonOut])
def read_all(db: Session = Depends(get_session)):
    return list_people(db)


@app.get("/people/{person_id}", response_model=PersonOut)
def read_one(person_id: int, db: Session = Depends(get_session)):
    person = get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.put("/people/{person_id}", response_model=PersonOut)
def update(person_id: int, person: PersonCreate, db: Session = Depends(get_session)):
    person_obj = update_person(db, person_id, name=person.name, email=person.email)
    return person_obj


@app.delete("/people/{person_id}", status_code=204)
def delete(person_id: int, db: Session = Depends(get_session)):
    delete_person(db, person_id)
    return None


__all__ = ["app"]
