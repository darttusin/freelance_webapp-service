import { Rating } from "react-simple-star-rating";

export function StarRating({ rate, className }) {
  return (
    <Rating
      className={className}
      size={"15px"}
      initialValue={rate}
      readonly={true}
    />
  );
}
