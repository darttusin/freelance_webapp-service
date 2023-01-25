import "./AdvertsCard.css";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";
import { deleteOffer } from "../../../http/adverts";

export const AdvertsCard = (props) => {
  const mode = localStorage.getItem("mode");
  const userId = localStorage.getItem("id");
  const navigate = useNavigate();
  const {
    advert_id,
    advert_price,
    advert_text,
    advert_title,
    isOffer,
    refetch,
  } = props;

  const onOfferDelete = async (e) => {
    e.stopPropagation();
    const data = {
      user_id: userId,
      advert_id: advert_id,
      offer_status: 6,
    };
    await deleteOffer(data);
    refetch();
  };
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
          {isOffer && (
            <p
              onClick={onOfferDelete}
              className="adverts-additional-header__close">
              x
            </p>
          )}
        </div>
        <p className="adverts-additional__price">{advert_price} Р</p>
        <p className="adverts-additional__desctiption">{advert_text}</p>
      </div>
    </div>
  );
};
