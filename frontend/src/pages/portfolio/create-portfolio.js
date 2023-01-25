import arrowBack from "../../icons/back-arrow.svg";
import { useNavigate } from "react-router-dom";
import { Layout } from "../../components/Layout/Layot";
import { Button } from "../../components/Button/Button";
import { useState } from "react";
import "../../styles/portfolio-page.css";
import { newPortfolio } from "../../http/portfolio";

export const CreatePortfolio = () => {
  const navigate = useNavigate();
  const [data, setData] = useState({
    portfolio_title: "",
    portfolio_description: "",
    portfolio_img_url: "",
  });

  const createPortfolio = async () => {
    const response = await newPortfolio(data);
    if (response.status == 200) {
      navigate(`/portfolio/${response.data.portfolio_id}`);
    }
  };
  return (
    <Layout withFooter={true}>
      <div className="portfolio-page">
        <div className="portfolio-page-header">
          <img
            src={arrowBack}
            className="arrow-back"
            alt="goback"
            onClick={() => {
              navigate(-1);
            }}
          ></img>
        </div>
        <p className="portfolio-page__label">Название</p>
        <input
          name="portfolio_title"
          className="portfolio-page__input"
          value={data.portfolio_title}
          onChange={(e) =>
            setData((prev) => ({ ...prev, [e.target.name]: e.target.value }))
          }
        />
        <p className="portfolio-page__label">Картинка</p>
        <div className="portfolio-page-additional">
          <input type={"file"} className="portfolio-page__input" />
          <p className="portfolio-page__label">Описание</p>
          <textarea
            name="portfolio_description"
            className="portfolio-page__input"
            value={data.description}
            onChange={(e) =>
              setData((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
          />

          <Button
            className={"portfolio-page__button"}
            text={"создать"}
            onClick={createPortfolio}
            style="white"
          />
        </div>
      </div>
    </Layout>
  );
};
