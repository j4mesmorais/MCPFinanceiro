import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from services.people import (
    create_person,
    get_person,
    list_people,
    update_person,
    delete_person,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_and_get_person(session):
    person = create_person(session, name="John Doe", email="john@example.com")
    fetched = get_person(session, person.id)
    assert fetched is not None
    assert fetched.name == "John Doe"
    assert fetched.email == "john@example.com"


def test_list_people(session):
    create_person(session, name="Alice", email="alice@example.com")
    create_person(session, name="Bob", email="bob@example.com")
    people = list_people(session)
    assert len(people) == 2


def test_update_person(session):
    person = create_person(session, name="Jane", email="jane@example.com")
    updated = update_person(session, person.id, name="Janet")
    assert updated.name == "Janet"
    fetched = get_person(session, person.id)
    assert fetched.name == "Janet"


def test_delete_person(session):
    person = create_person(session, name="Mark", email="mark@example.com")
    delete_person(session, person.id)
    assert get_person(session, person.id) is None
