from .data_base import Base
from .data_base import SQLALCHEMY_DATABASE_URL
from .data_base import engine
from .data_base import local_session
from .supabase_storage import get_all_buckets, get_all_files, upload_file


def get_database():
    database = local_session()
    try:
        yield database
    finally:
        database.close()


def create_models():
    Base.metadata.create_all(bind=engine)
