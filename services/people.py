"""Service layer for managing Person entities."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.mcp_financeiro.models import Person


def create_person(db: Session, name: str, email: str) -> Person:
    person = Person(name=name, email=email)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_person(db: Session, person_id: int) -> Person | None:
    return db.query(Person).filter(Person.id == person_id).first()


def list_people(db: Session) -> list[Person]:
    return db.query(Person).all()


def update_person(db: Session, person_id: int, **kwargs) -> Person:
    person = db.query(Person).filter(Person.id == person_id).one()
    for key, value in kwargs.items():
        if hasattr(person, key):
            setattr(person, key, value)
    db.commit()
    db.refresh(person)
    return person


def delete_person(db: Session, person_id: int) -> None:
    person = db.query(Person).filter(Person.id == person_id).one()
    db.delete(person)
    db.commit()
