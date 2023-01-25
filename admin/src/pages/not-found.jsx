import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

export const NotFound = () => {
  const navigate = useNavigate();

  const styleWrapper = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background: "#4c7daa",
    width: "100vw",
    height: "100vh",
  };

  const styleTitle = {
    fontSize: "120px",
    marginBottom: "20px",
    lineHeight: "100px",
  };

  const styleButton = {
    width: "200px",
  };

  return (
    <div style={styleWrapper}>
      <p style={styleTitle}>404</p>
      <Button
        style={styleButton}
        onClick={() => {
          navigate("/");
        }}
        variant="primary">
        Go home
      </Button>
    </div>
  );
};
