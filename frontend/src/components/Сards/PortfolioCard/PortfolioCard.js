import { useNavigate } from "react-router-dom";
import "./PortfolioCard.css";

export const PortfolioCard = ({ title, description, preview, id }) => {
  const navigate = useNavigate();
  return (
    <div
      onClick={() => navigate(`/portfolio/${id}`)}
      className="portfolio-card"
    >
      <img className="portfolio-card__img" src={preview} alt="preview"></img>
      <div className="portfolio-card-text">
        <p className="portfolio-card__title">{title}</p>
      </div>
    </div>
  );
};
