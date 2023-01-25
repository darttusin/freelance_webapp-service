import "./FeedbackCard.css";
import yellowStar from "../../../icons/star-yellow.svg";
import blackStar from "../../../icons/star-black.svg";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";
import { StarRating } from "../../StarRating/StarRating";

export const FeedbackCard = ({
  review_author_id,
  advert_title,
  review_id,
  review_author_comment,
  estimation,
}) => {
  const navigate = useNavigate();
  return (
    <div
      onClick={() => {
        navigate(`/review/${review_id}`);
      }}
      className="feedback-card">
      <div className="feedback__image">
        <img
          alt=""
          src={avatar}></img>
      </div>
      <div className="feedback-additional">
        <p className="feedback-additional__title">{advert_title}</p>
        <p className="feedback-additional__description">
          {review_author_comment}
        </p>
        <div className="feedback-marks">
          <StarRating
            readonly={true}
            rating={estimation}
          />
        </div>
      </div>
    </div>
  );
};
