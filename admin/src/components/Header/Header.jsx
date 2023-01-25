import { CustomDropDown } from "../DropDown/DropDown";
import "./Header.scss";

export const Header = ({ page }) => {
  return (
    <header className="header">
      <p className="header__title">{page}</p>
      <div className="header-user">
        <CustomDropDown />
        <img className="header-user__image"></img>
      </div>
    </header>
  );
};
