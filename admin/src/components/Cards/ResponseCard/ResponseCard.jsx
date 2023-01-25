import { useNavigate } from "react-router-dom";
import avatar from "../../../images/avatar.png";
import "./ResponseCard.scss";

export const ResponseCard = ({
  user_name,
  response_text,
  response_price,
  user_id,
}) => {
  const navigate = useNavigate();

  const onResponseClick = () => {
    navigate(`/users/${user_id}`);
  };
  return (
    <div
      className="response-card"
      onClick={onResponseClick}>
      <img
        src={avatar}
        alt=""
        className="response-card__image"
      />
      <div className="response-card-text">
        <p className="response-card__author">{user_name}</p>
        <p className="response-card__text">{response_text}</p>
        <p className="response-card__price">{response_price} Р</p>
      </div>
    </div>
  );
};
