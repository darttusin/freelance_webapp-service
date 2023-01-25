import "./Button.css";

export const Button = ({ style, text, onClick, className }) => {
  return (
    <>
      {style === "blue" && (
        <button onClick={onClick} className={`button_blue ${className}`}>
          {text}
        </button>
      )}
      {style === "black" && (
        <button onClick={onClick} className={`button_black ${className}`}>
          {text}
        </button>
      )}
      {style === "white" && (
        <button onClick={onClick} className={`button_white ${className}`}>
          {text}
        </button>
      )}
    </>
  );
};
