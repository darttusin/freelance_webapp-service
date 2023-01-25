from pydantic import BaseModel


class NewChat(BaseModel):
    advert_id: str
    customer_id: str
    performer_id: str
