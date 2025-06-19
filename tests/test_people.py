import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

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
    person = create_person(
        session,
        name="John Doe",
        email="john@example.com",
        celular="9999",
        endereco="Rua A",
        tipo="C",
        status="Ativo",
        cpf_cnpj="12345678901",
        dt_nascimento=date(1990, 1, 1),
    )
    fetched = get_person(session, person.id)
    assert fetched is not None
    assert fetched.name == "John Doe"
    assert fetched.email == "john@example.com"
    assert fetched.celular == "9999"
    assert fetched.endereco == "Rua A"
    assert fetched.tipo == "C"
    assert fetched.status == "Ativo"
    assert fetched.cpf_cnpj == "12345678901"
    assert fetched.dt_nascimento == date(1990, 1, 1)


def test_list_people(session):
    create_person(session, name="Alice")
    create_person(session, name="Bob")
    people = list_people(session)
    assert len(people) == 2


def test_update_person(session):
    person = create_person(session, name="Jane")
    updated = update_person(session, person.id, celular="12345")
    assert updated.celular == "12345"
    fetched = get_person(session, person.id)
    assert fetched.celular == "12345"


def test_delete_person(session):
    person = create_person(session, name="Mark", email="mark@example.com")
    delete_person(session, person.id)
    assert get_person(session, person.id) is None
