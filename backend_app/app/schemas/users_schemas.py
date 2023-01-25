from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    password: str 


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str 
    tg_name: str
    role: str


class ChangeInfo(BaseModel):
    user_name: str
    img_url: str
    description: str


class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    user_img_url: str | None   


class PerformerInfo(BaseModel):
    user_id: str
    user_info: dict
    avg_estimation: int
    count_estimation: int
