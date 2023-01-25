from pydantic import BaseModel, EmailStr


class AdminLogin(BaseModel):
    admin_email: str
    admin_password: str
    