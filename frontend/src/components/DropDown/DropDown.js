import "./DropDown.css";

export const DropDownItem = ({ children, onClick }) => {
  return (
    <p onClick={onClick} className="dropdown__item">
      {children}
    </p>
  );
};
export const DropDown = ({ children, withoutBorder }) => {
  return (
    <div className={`dropdown ${withoutBorder && "dropdown_no-border"}`}>
      {children}
    </div>
  );
};
