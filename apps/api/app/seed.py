from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base
from app.models.user import User


def create_demo_data(db: Session) -> None:
    if db.execute(select(User).limit(1)).first():
        return
    db.add(User(email="admin@acme.com", hashed_password=hash_password("admin123!"), role="admin"))
    db.add(User(email="analyst@acme.com", hashed_password=hash_password("analyst123!"), role="analyst"))
    db.commit()


def initialize_database(engine) -> None:
    Base.metadata.create_all(bind=engine)