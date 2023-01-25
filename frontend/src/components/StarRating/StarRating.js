import React, { useState } from "react";
import { Rating } from "react-simple-star-rating";

export function StarRating({ rating, readonly, onRatingClick }) {
  return (
    <div className="App">
      <Rating
        onClick={onRatingClick}
        readonly={readonly}
        initialValue={rating}
        size={"20px"}
      />
    </div>
  );
}
