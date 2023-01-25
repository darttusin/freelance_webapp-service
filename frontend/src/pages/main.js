import { Layout } from "../components/Layout/Layot";
import "../styles/main.css";
import { Button } from "../components/Button/Button";
import { useNavigate } from "react-router-dom";

export const Main = () => {
  const navigate = useNavigate();
  return (
    <Layout>
      <div className="main-page">
        <h1 className="main-page__title">
          Создавайте, берите и,находите заказы прямо сейчас!
        </h1>
        <Button
          style="white"
          onClick={() => navigate("/profile")}
          text="начать"></Button>
      </div>
    </Layout>
  );
};
