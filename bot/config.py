import asyncio
import os

import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


BOT_TOKEN = os.environ.get('BOT_TOKEN')
APP_URL = os.environ.get('APP_URL')
DBUSER = os.environ.get('DBUSER')
DBPASSWORD = os.environ.get('DBPASSWORD')
DBHOST = os.environ.get('DBHOST')
DBNAME = os.environ.get('DBNAME')
DBPORT = os.environ.get('DBPORT')


url = "postgresql+asyncpg:/"+\
                f"/{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"
engine = create_async_engine(url, future=True, echo=False)
async_session = sessionmaker(
                engine, expire_on_commit=False, class_=AsyncSession)