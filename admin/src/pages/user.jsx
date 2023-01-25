import { MainLayout } from "../Layouts/MainLayout";
import "../styles/user.scss";
import avatar from "../images/avatar.png";
import { AdvertCard } from "../components/Cards/AdvertCard/AdvertCard";
import { ReviewCard } from "../components/Cards/ReviewCard/ReviewCard";
import { useQuery } from "react-query";
import { getUser } from "../api/user";
import { useParams } from "react-router-dom";
import { Spinner } from "react-bootstrap";

export const User = () => {
  const { id } = useParams();
  const { data, isLoading } = useQuery(["user", id], () => getUser(id));

  if (isLoading) {
    return (
      <MainLayout page={"Пользователь"}>
        <Spinner />
      </MainLayout>
    );
  }
  return (
    <MainLayout page={"Пользователь"}>
      <div className="user-row">
        <div className="user-information">
          <div className="user-additional">
            <img
              className="user-image"
              src={avatar}
              alt="user avatar"
            />
            <div className="user-text">
              <div className="user-information__title">
                {data.user_info[0].user_name}
              </div>
              {/* <div className="user-text__item">
                <p className="user-text__key">Номер</p>
                <p className="user-text__value">+7999999999</p>
              </div> */}
              <div className="user-text__item">
                <p className="user-text__key">Почта</p>
                <p className="user-text__value">
                  {data.user_info[0].user_email}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="user-statistics">
          <p className="user-title user-statistics__title">Статистика</p>
          <p className="user-statistics__item">
            {data.count_adverts} объявлений
          </p>
          <p className="user-statistics__item">{data.count_views} отзывов</p>
          {/* <p className="user-statistics__item">15 жалоб</p> */}
          <p className="user-statistics__item">
            {data.count_all_responses} откликов
          </p>
          <p className="user-statistics__item">
            {data.count_all_finished_offers} сделок
          </p>
        </div>
      </div>
      <div className="user-row">
        <div className="user-adverts">
          <p className="user-adverts__title user-title">Объявления</p>
          <div className="user-adverts-items">
            {data.adverts.length ? (
              data.adverts.map((advert) => <AdvertCard {...advert} />)
            ) : (
              <p>У пользователя нет объявлений</p>
            )}
          </div>
        </div>
        <div className="user-reviews">
          <p className="user-reviews__title user-title">Отзывы</p>
          <div className="user-reviews-items">
            {data.reviews.length ? (
              data.reviews.map((review) => <ReviewCard {...review} />)
            ) : (
              <p>У пользователя нет отзывов</p>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};
