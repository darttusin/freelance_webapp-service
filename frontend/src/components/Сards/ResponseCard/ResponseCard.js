import "./ResponseCard.css";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

export const ResponseCard = ({
  advert_price,
  advert_text,
  advert_title,
  advert_id,
  response_status,
}) => {
  const [status, setStatus] = useState("Ожидание");

  const navigate = useNavigate();

  useEffect(() => {
    if (response_status == "added on website") {
      setStatus("Ожидание");
    }

    if (response_status == "in working") {
      setStatus("В работе");
    }
  }, [response_status]);

  return (
    <div
      className="response-card"
      onClick={() => navigate(`/advert/${advert_id}`)}>
      <div className="response-img">
        <img
          src={avatar}
          alt=""
        />
      </div>
      <div className="response-additional">
        <div className="response-additional-header">
          <p className="response-additional__title">{advert_title}</p>
          <button className="response-additional__status">{status}</button>
        </div>
        <p className="response-additional__price">{advert_price} Р</p>
        <p className="response-additional__desctiption">{advert_text}</p>
      </div>
    </div>
  );
};
