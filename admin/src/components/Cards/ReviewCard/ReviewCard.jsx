import { StarRating } from "../../StarRating/StarRating";
import "./ReviewCard.scss";

export const ReviewCard = () => {
  return (
    <div className="review">
      <p className="review__author">Георгий</p>
      <p className="review__text">
        Данный исполнитель отработал очень хорошоДанный исполнитель отработал
        очень хорошоДанный исполнитель отработал очень хорошоДанный исполнитель
        отработал очень хорошоДанный исполнитель отработал очень хорошоДанный
        исполнитель отработал очень хорошоДанный исполнитель отработал очень
      </p>
      <StarRating
        rate={5}
        className={"review__rating"}
      />
    </div>
  );
};
