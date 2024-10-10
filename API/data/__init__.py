from .data_base import Base
from .data_base import local_session
from .data_base import engine
from .data_base import SQLALCHEMY_DATABASE_URL

def get_database():
    database = local_session()
    try:
        yield database
    finally:
        database.close()


def create_models():
    Base.metadata.create_all(bind=engine)