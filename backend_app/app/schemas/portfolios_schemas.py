from pydantic import BaseModel


class NewPortfolio(BaseModel):
    portfolio_title: str
    portfolio_description: str
    portfolio_img_url: str


class UpdatePortfolio(BaseModel):
    portfolio_id: str
    portfolio_title: str
    portfolio_description: str
    portfolio_img_url: str


class PortfolioInfo(BaseModel):
    portfolio_id: str
    portfolio_title: str
    portfolio_description: str
    portfolio_img_url: str | None   