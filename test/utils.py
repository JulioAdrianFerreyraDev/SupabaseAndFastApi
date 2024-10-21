import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

from app import ProductionBase
from app.models import UserModel

__SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

__engine = create_engine(__SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=__engine)


def create_all_models():
    ProductionBase.metadata.create_all(bind=__engine)


def override_get_database():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_user_dependency():
    return {"username": "julioferreyra", "id": 1, "role": "user"}


@pytest.fixture
def test_admin():
    user: UserModel = UserModel(
        username="julioferreyra",
        password="jafete210403",
        first_name="julio",
        last_name="ferreyra",
        role="admin",
        email="julio@ferreyra.com"
    )
    user.user_id = 1
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with __engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_user():
    user: UserModel = UserModel(
        username="julioferreyra",
        password="jafete210403",
        first_name="julio",
        last_name="ferreyra",
        role="user",
        email="julio@ferreyra.com"
    )
    user.user_id = 1
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with __engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
