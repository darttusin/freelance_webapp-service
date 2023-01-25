import "../AdvertsCard/AdvertsCard.css";
import "./JobOfferCard.css";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";

export const JobOfferCard = (props) => {
  const {
    activeIndex,
    advert_id,
    advert_price,
    advert_text,
    advert_title,
    advert_status,
    value,
    index,
    onOfferClick,
  } = props;
  return (
    <div
      className={`adverts-card ${
        index == activeIndex ? "jobOfferCard_active" : ""
      }`}
      onClick={() => onOfferClick(advert_id, index)}>
      <div className="adverts-img">
        <img
          src={avatar}
          alt=""
        />
      </div>
      <div className="adverts-additional">
        <div className="adverts-additional-header">
          <p className="adverts-additional__title">{advert_title}</p>
        </div>
        <p className="adverts-additional__price">{advert_price} Р</p>
        <p className="adverts-additional__desctiption">{advert_text}</p>
      </div>
    </div>
  );
};
