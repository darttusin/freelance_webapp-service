import "./Input.css";

export const Input = ({ label, placeholder, onChange, type, name }) => {
  return (
    <div className="input">
      <p className="input__text">{label}</p>
      <input
        name={name}
        onChange={onChange}
        type={type ? type : "text"}
        className="input__area"
        placeholder={placeholder}
      ></input>
    </div>
  );
};
