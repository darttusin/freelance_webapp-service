from pydantic import BaseModel


class AddResponse(BaseModel):
    advert_id: str
    responce_text: str
    price: int


class UpdateStatus(BaseModel):
    user_id: str
    advert_id: str
    response_status: str


class UpdateStatusOffer(BaseModel):
    user_id: str
    advert_id: str
    offer_status: str


class OfferJob(BaseModel):
    user_id: str
    advert_id: str


class ResponseInfo(BaseModel):
    advert_id: str
    advert_title: str
    advert_text: str
    advert_price: float
    advert_city: str
    response_status: str


class PortfolioInfo(BaseModel):
    advert_id: str
    advert_title: str
    advert_text: str
    advert_city: str
    advert_price: float
    value: str
    offer_status: str