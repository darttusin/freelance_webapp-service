from fastapi import APIRouter
from typing import List
import psycopg2

import app.constants.enviroment as env


checks_routers = APIRouter()


# @checks_routers.put(
#     "/db/{table_name}"
# )
# async def db_check(
#     table_name: str
# ) -> List:
#     connection = psycopg2.connect(
#         user=env.DBUSER, 
#         password=env.DBPASSWORD, 
#         database=env.DBNAME, 
#         host=env.DBHOST, 
#         port=env.DBPORT
#     )

#     curs = connection.cursor()
#     curs.execute(f"SELECT * FROM {table_name}")
#     row = curs.fetchall()
#     connection.close()

#     return row


@checks_routers.get(
    "/init"
)
async def init() -> dict:
    return {
        "performers_filters": [
            "raiting",
            "count_reviews",
            "count_jobs"    
        ],
        "adverts_filters": [
            "city",
            "category"
        ]
    }
