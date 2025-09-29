from sqlalchemy import Table, Column, MetaData, Integer, String, Text, create_engine, Identity
from sqlalchemy.exc import SQLAlchemyError

from config_reader import settings

db_host = "localhost"
db_port = 5433
db_name = settings.POSTGRES_DB
db_user = settings.POSTGRES_USER
db_password = settings.POSTGRES_PASSWORD.get_secret_value()

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url, echo=True, isolation_level="REPEATABLE READ")

metadata = MetaData()

posts_table = Table(
    "raw_users_by_posts", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(128), nullable=False),
    Column("body", Text, nullable=False),
    Column("user_id", Integer, nullable=False),
)

try:
    metadata.create_all(engine)
    print("Таблица 'posts' успешно создана!")

except SQLAlchemyError as e:
    print(f"Ошибка при подключении к базе данных или создании таблицы: {e}")
