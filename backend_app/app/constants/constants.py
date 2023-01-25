import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = os.environ.get('SECRET_KEY', "SECRET")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="admin/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")