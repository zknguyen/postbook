import os

from sqlalchemy import create_engine, URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    URL.create(
        drivername=f"{os.getenv('POSTGRES_DRIVERNAME')}",
        username=f"{os.getenv('POSTGRES_USERNAME')}",
        password=f"{os.getenv('POSTGRES_PASSWORD')}",
        host=f"{os.getenv('POSTGRES_HOST')}",
        port=os.getenv('POSTGRES_POST'),
        database=f"{os.getenv('POSTGRES_DATABASE')}",
    )
)

async_engine = create_async_engine(
    URL.create(
        drivername=f"{os.getenv('POSTGRES_ASYNC_DRIVERNAME')}",
        username=f"{os.getenv('POSTGRES_USERNAME')}",
        password=f"{os.getenv('POSTGRES_PASSWORD')}",
        host=f"{os.getenv('POSTGRES_HOST')}",
        port=os.getenv('POSTGRES_POST'),
        database=f"{os.getenv('POSTGRES_DATABASE')}",
    )
)


Base = declarative_base()
Base.metadata.create_all(engine)
