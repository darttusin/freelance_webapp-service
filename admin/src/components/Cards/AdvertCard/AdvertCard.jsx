import { useNavigate } from "react-router-dom";
import "./AdvertCard.scss";

export const AdvertCard = ({
  advert_id,
  advert_title,
  advert_status,
  advert_text,
  advert_price,
}) => {
  const navigate = useNavigate();
  const onAdvertClick = () => {
    navigate(`/advert/${advert_id}`);
  };
  return (
    <div
      className="advert-card"
      onClick={onAdvertClick}>
      <p className="advert-card__title">{advert_title}</p>
      <p className="advert-card__description">{advert_text}</p>
      <p className="advert-card__price">{advert_price} Р</p>
    </div>
  );
};
