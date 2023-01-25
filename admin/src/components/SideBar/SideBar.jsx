import { useNavigate } from "react-router-dom";
import { SideBarLink } from "./SideBarLink";
import "./Sidebar.scss";

const links = [
  // { name: "Главная", path: "/" },
  { name: "Создание пользователя", path: "/create-user" },
  { name: "Пользователи", path: "/users" },
  // { name: "Чаты", path: "/chats" },
];

export const SideBar = () => {
  const navigate = useNavigate();
  return (
    <>
      <div className="sidebar-push"></div>
      <div className="sidebar">
        <p
          onClick={() => navigate("/users")}
          className="sidebar__title">
          Freelance-web-app
        </p>
        <div className="sidebar-links">
          {links.map((link, index) => (
            <SideBarLink
              key={index}
              {...link}
            />
          ))}
        </div>
      </div>
    </>
  );
};
