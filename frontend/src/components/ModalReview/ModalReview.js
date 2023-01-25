import { Button } from "../Button/Button";
import { PageHeader } from "../PageHeader/PageHeader";
import avatar from "../../img/avatar.png";
import "./ModalReview.css";
import { StarRating } from "../StarRating/StarRating";
import { useState } from "react";
import { addReview } from "../../http/review";
import { finishWork, updateResponse } from "../../http/adverts";
import { useNavigate } from "react-router-dom";

export const ModalReview = ({ setModalReview, user_id, advert_id }) => {
  const navigate = useNavigate();
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");

  const handleArrow = () => {
    setModalReview((prev) => ({ ...prev, show: false }));
  };

  const onRatingClick = (value) => {
    setRating(value);
  };
  const onFinishClick = async () => {
    const data = {
      review_author_comment: comment,
      estimation: rating,
      advert_id: advert_id,
      user_id: user_id,
    };
    if (comment) {
      await addReview(data);
      setModalReview((prev) => ({ ...prev, show: false }));
      await finishWork(advert_id);
      navigate("/chat");
    }
  };

  return (
    <div className="modal-response-wrapper">
      <div className="modal-response-content">
        <PageHeader
          handleArrow={handleArrow}
          withDots={false}
        />
        <div>
          <div className="modal-review-body">
            <div className="modal-review-text">
              <p className="modal-review-text__title">Отзыв о "тевирп" </p>
              <textarea
                onChange={(e) => setComment(e.target.value)}
                className="modal-review-text__area"></textarea>
            </div>
          </div>
        </div>
        <div className="modal-review-footer">
          <StarRating
            onRatingClick={onRatingClick}
            rating={rating}
            readonly={false}
          />
          <Button
            onClick={onFinishClick}
            className="modal-review-footer__button"
            style="black"
            text={"Оставить отзыв и завершить сделку"}></Button>
        </div>
      </div>
    </div>
  );
};
