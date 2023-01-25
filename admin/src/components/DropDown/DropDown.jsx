import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { useNavigate } from "react-router-dom";
import { setCookie } from "../../utils/cookie";
import "./DropDown.scss";

export const CustomDropDown = () => {
  const username = localStorage.getItem("name");
  const navigate = useNavigate();
  const onLogoutClick = () => {
    setCookie("access_token", "");
    window.location.reload();
    navigate("/");
  };
  return (
    <DropdownButton
      className="dropdown-button"
      align="end"
      title={username}
      id="dropdown-menu-align-end">
      <Dropdown.Item
        onClick={onLogoutClick}
        eventKey="1">
        Logout
      </Dropdown.Item>
    </DropdownButton>
  );
};
