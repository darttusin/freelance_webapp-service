import arrowBack from "../../icons/back-arrow.svg";
import dots from "../../icons/dots.svg";
import { useNavigate } from "react-router-dom";

export const PageHeader = ({ handleArrow, onDotsClick, withDots = true }) => {
  const navigate = useNavigate();
  return (
    <div className="page-header">
      <img
        src={arrowBack}
        className="arrow-back"
        alt="goback"
        onClick={handleArrow}
      ></img>
      {withDots && (
        <img src={dots} className="dots" alt="dots" onClick={onDotsClick}></img>
      )}
    </div>
  );
};
