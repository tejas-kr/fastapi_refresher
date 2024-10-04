import os
from logger import logger
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

DATABASE_URL: str = os.getenv("DB_URL")
logger.info(f"Database URL: {DATABASE_URL}")

if not DATABASE_URL:
    logger.error("Error connecting to the database - Database URL is not set")
    raise RuntimeError("Error connecting to the database")

try:
    engine = create_engine(DATABASE_URL, echo=True)
except SQLAlchemyError as sql_al_err:
    logger.exception(sql_al_err)
    raise sql_al_err


def init_db():
    """
    This function is not needed with alembic.
    Initialize the DB and create the table schema
    :return: None
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yields the DB Session
    :yield: DB Session
    """
    with Session(engine) as session:
        yield session
