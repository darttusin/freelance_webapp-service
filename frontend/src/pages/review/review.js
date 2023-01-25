import { Layout } from "../../components/Layout/Layot";
import { PageHeader } from "../../components/PageHeader/PageHeader";
import yellowStar from "../../icons/star-yellow.svg";
import blackStar from "../../icons/star-black.svg";
import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import { getReview } from "../../http/review";
import "../../styles/review.css";
import { StarRating } from "../../components/StarRating/StarRating";

export const Review = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: review, isLoading } = useQuery(["review", id], () =>
    getReview(id)
  );

  const handleArrow = () => {
    navigate(-1);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Layout withFooter={true}>
      <div className="review">
        <PageHeader
          withDots={false}
          handleArrow={handleArrow}
        />
        <h1 className="page__title review__title">{review.user_name}</h1>
        <p className="review__work-type">{review.advert_title} </p>
        <p className="review__description">{review.review_author_comment}</p>
        <div className="review-marks">
          <p className="review-marks__title">Оценка: </p>
          <div className="review__feedback">
            <StarRating
              rating={review.estimation}
              readonly={true}
            />
          </div>
        </div>
      </div>
    </Layout>
  );
};
