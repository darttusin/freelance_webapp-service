import { useLocation, useNavigate } from "react-router-dom";

export const SideBarLink = ({ name, path }) => {
  const navigate = useNavigate();
  const pathname = useLocation().pathname;

  const onLinkClick = () => {
    navigate(path);
  };

  const isActive = () => {
    if (pathname.includes(path) && path.length > 1) return true;
    if (pathname == path) return true;
  };
  return (
    <div
      onClick={onLinkClick}
      className={`sidebar-links__item ${
        isActive(path) ? "sidebar-links__item_active" : ""
      }`}>
      {name}
    </div>
  );
};
