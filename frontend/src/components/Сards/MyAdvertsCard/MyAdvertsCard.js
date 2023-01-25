import "./MyAdvertsCard.css";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export const MyAdvertsCard = (props) => {
  const {
    advert_city,
    advert_id,
    advert_text,
    advert_price,
    advert_title,
    advert_status,
    value,
  } = props;
  const [status, setStatus] = useState("Ожидание");
  const navigate = useNavigate();

  useEffect(() => {
    if (advert_status == "added on website") {
      setStatus("Ожидание");
    }

    if (advert_status == "in working") {
      setStatus("В работе");
    }
  }, [advert_status]);

  return (
    <div
      onClick={() => navigate(`/advert/${advert_id}`)}
      className="adverts-card">
      <div className="adverts-img">
        <img
          src={avatar}
          alt=""
        />
      </div>
      <div className="adverts-additional">
        <div className="adverts-additional-header">
          <p className="adverts-additional__title">{advert_title}</p>
          <button className="response-additional__status">{status}</button>
        </div>
        <p className="adverts-additional__price">{advert_price}$</p>
        <p className="adverts-additional__desctiption">{advert_text}</p>
      </div>
    </div>
  );
};
