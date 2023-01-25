import avatar from "../../img/avatar.png";
import dots from "../../icons/dots.svg";
import "./AdvertResponse.css";
import { createChat } from "../../http/chat";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export const AdvertResponse = (props) => {
  const navigate = useNavigate();
  const [isDropDown, setIsDropDown] = useState(false);
  const {
    response_price,
    response_text,
    user_id,
    user_img_url,
    user_name,
    setModalResponse,
  } = props;

  const onDotsClick = (e) => {
    e.stopPropagation();
    setIsDropDown(true);
  };

  const handleSetPerfomer = () => {
    setIsDropDown(false);
    setModalResponse((prev) => ({
      ...prev,
      user_id: user_id,
      show: true,
      user_name: user_name,
      response_price: response_price,
      response_text: response_text,
    }));
  };

  const navigateToProfile = () => {
    navigate(`/profile/${user_id}`);
  };
  return (
    <div className="advert-response">
      {isDropDown && (
        <div
          onClick={(e) => e.stopPropagation()}
          className="advert-response-dropdown">
          <p
            onClick={handleSetPerfomer}
            className="advert-response-dropdown__item">
            Назначить исполнителем
          </p>
          <p
            onClick={navigateToProfile}
            className="advert-response-dropdown__item">
            Перейти в профиль
          </p>
          <p
            onClick={() => setIsDropDown(false)}
            className="advert-response-dropdown__item">
            Отменить
          </p>
        </div>
      )}

      <div className="advert-reponse-header">
        <span className="advert-response__username">{user_name}</span>
        <span className="advert-response__price">{response_price} Р</span>
      </div>
      <div className="advert-response-body">
        <p className="advert-response__description">{response_text}</p>
        <img
          className="advert-response__image"
          src={avatar}
          alt="user avatar"
        />
      </div>
      <img
        src={dots}
        onClick={onDotsClick}
        className="advert-response__dots"
        alt=""
      />
    </div>
  );
};
