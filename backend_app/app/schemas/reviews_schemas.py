from pydantic import BaseModel


class AddReview(BaseModel):
    user_id: str
    advert_id: str
    review_author_comment: str
    estimation: int
