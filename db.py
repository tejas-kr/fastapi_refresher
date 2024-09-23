from sqlmodel import create_engine, SQLModel, Session


DATABASE_URL = 'sqlite:///db.sqlite'

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """
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
