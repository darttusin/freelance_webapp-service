from pydantic import BaseModel, validator


class NewAdvert(BaseModel):
    advert_text: str
    advert_title: str
    advert_category: str
    advert_city: str
    advert_price: int


class AdvertUpdate(BaseModel):
    advert_text: str
    advert_title: str
    advert_category: str
    advert_city: str
    advert_price: int


class AdvertInfo(BaseModel):
    advert_id: str
    advert_title: str
    advert_city: str
    advert_text: str
    advert_price: float
    value: str 
    response: bool
    user_img_url: str | None


class MyAdvertInfo(BaseModel):
    advert_id: str
    advert_title: str
    advert_city: str
    advert_text: str
    advert_price: float
    value: str 
    advert_status: str
    user_img_url: str | None
    user_id: str | None