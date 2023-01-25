import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "react-query";
import { Layout } from "../../components/Layout/Layot";
import avatar from "../../img/avatar.png";
import yellowStar from "../../icons/star-yellow.svg";
import preview from "../../img/preview.jpg";
import blackStar from "../../icons/star-black.svg";
import { PortfolioCard } from "../../components/Сards/PortfolioCard/PortfolioCard";
import { FeedbackCard } from "../../components/Сards/FeedbackCard/FeedbackCard";
import { CustomSlider } from "../../components/Slider/CustomSlider";
import { DropDown } from "../../components/DropDown/DropDown";
import { DropDownItem } from "../../components/DropDown/DropDown";

import "../../styles/profile.css";
import { getProfile } from "../../http/user";
import { PageHeader } from "../../components/PageHeader/PageHeader";
import { JobOffer } from "../../components/JobOffer/JobOffer";
import { StarRating } from "../../components/StarRating/StarRating";

export const UserProfile = () => {
  const { userId } = useParams();
  const { data, isLoading } = useQuery(["user", userId], () =>
    getProfile(userId)
  );
  const [isDropDown, setIsDropDown] = useState(false);
  const [showJobOffering, setShowJobOffering] = useState(false);
  const navigate = useNavigate();

  const onDotsClick = () => {
    setIsDropDown(true);
  };

  const handleArrow = () => {
    navigate(-1);
  };

  const toggleOffer = () => {
    setShowJobOffering((prev) => !prev);
  };

  if (isLoading) {
    return "Loading....";
  }

  return (
    <Layout withFooter={true}>
      {showJobOffering && (
        <JobOffer
          toggleOffer={toggleOffer}
          userId={userId}
        />
      )}
      <div className="profile">
        {!isDropDown && (
          <PageHeader
            handleArrow={handleArrow}
            onDotsClick={onDotsClick}
          />
        )}
        {isDropDown && (
          <DropDown>
            <DropDownItem onClick={() => setIsDropDown(false)}>
              отменить
            </DropDownItem>
            <DropDownItem
              onClick={() => {
                setIsDropDown(false);
                toggleOffer();
              }}>
              Предложить работу
            </DropDownItem>
          </DropDown>
        )}
        <div className="profile__avatar">
          <img
            className=""
            alt=""
            src={avatar}
          />
        </div>
        <div className="profile-description">
          <p className="profile__name">{data.user_name}</p>
          <p className="profile__role">Role: {""}</p>
          <div className="profile__marks">
            <StarRating
              readonly={true}
              rating={4}
            />
            <p>425 оценок</p>
          </div>
        </div>

        <div className="profile-portfolio">
          <div className="profile__title profile-portfolio__title">
            <p>Портфолио</p>
          </div>
          <CustomSlider>
            {data.user_portfolios.map((item, index) => (
              <PortfolioCard
                key={index}
                title={item.portfolio_title}
                description={item.portfolio_description}
                preview={preview}
                id={item.portfolio_id}
              />
            ))}
          </CustomSlider>
        </div>
        <div className="profile-reviews">
          <p className="profile__title">Отзывы</p>
          {data.user_estimations.map((item) => (
            <FeedbackCard {...item} />
          ))}
        </div>
      </div>
    </Layout>
  );
};
