from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config_reader import settings

db_host = settings.POSTGRES_HOST
db_port = settings.POSTGRES_PORT
db_name = settings.POSTGRES_DB
db_user = settings.POSTGRES_USER
db_password = settings.POSTGRES_PASSWORD.get_secret_value()

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    db_url,
    echo=settings.SQLALCHEMY_ECHO_FLAG,
    isolation_level="REPEATABLE READ"
)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
