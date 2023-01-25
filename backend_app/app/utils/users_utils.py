import uuid
import hashlib
from jose import JWTError, jwt
import app.constants.constants as const
from datetime import datetime, timedelta


async def create_access_token(
    data: dict
):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=10080)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        const.SECRET_KEY, 
        algorithm=const.ALGORITHM
    )
    return encoded_jwt


def verify_password(
    plain_password: str, 
    hashed_password: str
):
    return const.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(
    password: str
):
    return const.pwd_context.hash(password)


async def generate_user_id(
    role: str
) -> str:
    _id = f'{role}_' + str(uuid.uuid4()).replace('-','')
    return _id


async def generate_post_id(
    post: str
) -> str:
    _id = f'{post}_' + str(uuid.uuid4().int)
    return _id
    