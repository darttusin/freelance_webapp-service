import { useNavigate } from "react-router-dom";
import { getCookie } from "../../utils/cookie";
import "./Header.css";

export const Header = () => {
  const navigate = useNavigate();
  const token = getCookie("access_token");
  return (
    <header className="header">
      <p
        className="header__logo"
        onClick={() => {
          navigate("/");
        }}
      >
        freelance-web-app
      </p>
      {!token ? (
        <div className="header-auth">
          <p className="header-auth__item" onClick={() => navigate("/login")}>
            Вход
          </p>
          <p
            className="header-auth__item"
            onClick={() => navigate("/registration")}
          >
            Регистрация
          </p>
        </div>
      ) : (
        ""
      )}
    </header>
  );
};
