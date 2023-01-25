import "./PerformersCard.css";
import yellowStar from "../../../icons/star-yellow.svg";
import blackStar from "../../../icons/star-black.svg";
import avatar from "../../../img/avatar.png";
import { useNavigate } from "react-router-dom";

export const PerformersCard = ({
  user_id,
  user_info,
  avg_estimation,
  count_estimation,
}) => {
  const navigate = useNavigate();
  return (
    <div
      onClick={() => {
        navigate(`/profile/${user_id}`);
      }}
      className="performers-card"
    >
      <div className="performers__image">
        <img alt="" src={avatar}></img>
      </div>
      <div className="performers-additional">
        <p className="performers-additional__title">{user_info?.user_name}</p>
        <p className="performers-additional__description">
          Специалист со стажем работы около трех лет в сфере WEB дизайна
        </p>
        <div className="performers-marks">
          <img alt="" src={yellowStar} />
          <img alt="" src={yellowStar} />
          <img alt="" src={yellowStar} />
          <img alt="" src={yellowStar} />
          <img alt="" src={blackStar} />
        </div>
      </div>
    </div>
  );
};
