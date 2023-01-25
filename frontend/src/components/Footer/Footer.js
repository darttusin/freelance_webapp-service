import "./Footer.css";
import board from "../../icons/1.svg";
import response from "../../icons/2.svg";
import chat from "../../icons/3.svg";
import cabinet from "../../icons/4.svg";
import { useLocation, useNavigate } from "react-router-dom";

export const Footer = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const mode = localStorage.getItem("mode")
    ? localStorage.getItem("mode")
    : (() => {
        localStorage.setItem("mode", "performer");
        return "performer";
      })();

  const isActive = (route) => {
    return location.pathname == route;
  };

  return (
    <footer className="footer-wrapper">
      <div className="footer">
        {mode == "performer" ? (
          <>
            <div
              onClick={() => navigate("/adverts", { state: { page: 1 } })}
              className={`footer-tab ${
                isActive("/adverts") && "footer-tab_active"
              }`}>
              <img
                className="tab__icon"
                src={board}
                alt="tab"></img>
              <p className="tab__title">Объявления</p>
            </div>
            <div
              onClick={() => navigate("/my-responses")}
              className={`footer-tab ${
                isActive("/my-responses") && "footer-tab_active"
              }`}>
              <img
                className="tab__icon"
                src={response}
                alt="tab"></img>
              <p className="tab__title">Мои отклики</p>
            </div>
          </>
        ) : (
          <>
            <div
              onClick={() => navigate("/performers")}
              className={`footer-tab ${
                isActive("/performers") && "footer-tab_active"
              }`}>
              <img
                className="tab__icon"
                src={board}
                alt="tab"></img>
              <p className="tab__title">Исполнители</p>
            </div>
            <div
              onClick={() => navigate("/my-adverts", { page: 1 })}
              className={`footer-tab footer-tab_big ${
                isActive("/my-adverts") && "footer-tab_active"
              }`}>
              <img
                className="tab__icon"
                src={response}
                alt="tab"></img>
              <p className="tab__title tab__title_small">Мои объявления</p>
            </div>
          </>
        )}
        <div
          onClick={() => navigate("/chat")}
          className={`footer-tab ${isActive("/chat") && "footer-tab_active"}`}>
          <img
            className="tab__icon"
            src={chat}
            alt="tab"></img>
          <p className="tab__title">Чат</p>
        </div>
        <div
          onClick={() => navigate("/profile")}
          className={`footer-tab ${
            isActive("/profile") && "footer-tab_active"
          }`}>
          <img
            className="tab__icon"
            src={cabinet}
            alt="tab"></img>
          <p className="tab__title">Мой профиль</p>
        </div>
      </div>
    </footer>
  );
};
