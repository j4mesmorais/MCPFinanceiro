"""Simple database migration script replacing Alembic."""

from database import Base, engine


def upgrade() -> None:
    """Create all tables defined in SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    upgrade()
