import app.constants.enviroment as env
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.models.models import base
import asyncpg
import psycopg2
import asyncio
    

url = f"postgresql+asyncpg://{env.DBUSER}:{env.DBPASSWORD}@{env.DBHOST}:{env.DBPORT}/{env.DBNAME}"

engine = create_async_engine(
    url, 
    future=True, 
    echo=False
)
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)



def db_insert_default_values():
    connection = psycopg2.connect(
        user=env.DBUSER, 
        password=env.DBPASSWORD, 
        database=env.DBNAME, 
        host=env.DBHOST, 
        port=env.DBPORT
    )
    commands = [
        "INSERT INTO statuses VALUES ('1', 'added on website');",
        "INSERT INTO statuses VALUES ('2', 'added response on advert');",
        "INSERT INTO statuses VALUES ('3', 'declined response');",
        "INSERT INTO statuses VALUES ('4', 'in working');",
        "INSERT INTO statuses VALUES ('5', 'offer a job');",
        "INSERT INTO statuses VALUES ('6', 'declined a job');",
        "INSERT INTO statuses VALUES ('7', 'work finished');",
        "INSERT INTO parameters VALUES('category', 'category of advert');",
    ]
    
    curs = connection.cursor()

    for com in commands:
        curs.execute(com)

    connection.commit()
    connection.close()


def db_create() -> None:
    if env.RESET_DB == "True":
        sync_url = f"postgresql://{env.DBUSER}:{env.DBPASSWORD}@{env.DBHOST}:{env.DBPORT}/{env.DBNAME}"
        sync_engine = create_engine(sync_url)
        base.metadata.drop_all(sync_engine)
        base.metadata.create_all(sync_engine)
        db_insert_default_values()
        print("Database reseted")
    else:
        print("Database up-to-date")
