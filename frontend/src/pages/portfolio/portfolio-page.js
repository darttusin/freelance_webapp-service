import preview from "../../img/preview.jpg";
import { useNavigate, useParams } from "react-router-dom";
import { Layout } from "../../components/Layout/Layot";

import { useState } from "react";
import { DropDown, DropDownItem } from "../../components/DropDown/DropDown";
import { Button } from "../../components/Button/Button";
import { PageHeader } from "../../components/PageHeader/PageHeader";
import { useQuery } from "react-query";
import {
  deletePortfolio,
  getPortfolio,
  updatePortfolio,
} from "../../http/portfolio";
import "../../styles/portfolio-page.css";

export const PortfolioPage = () => {
  const { id } = useParams();
  const [portfolio, setPortfolio] = useState();
  const [isEditing, setIsEditing] = useState(false);
  const [isDropDown, setIsDropDown] = useState(false);

  const navigate = useNavigate();

  const { isLoading, error } = useQuery(
    ["portfolio", id],
    () => getPortfolio(id),
    {
      onSuccess: setPortfolio,
    }
  );

  const savePortfolio = async () => {
    const response = await updatePortfolio(portfolio);
    setIsEditing(false);
  };

  const deleteThisPortfolio = async () => {
    const response = await deletePortfolio(id);
    navigate("/profile");
  };

  if (isLoading) {
    return "Loading...";
  }
  if (portfolio) {
    return (
      <Layout withFooter={true}>
        <div className="portfolio-page">
          <PageHeader
            handleArrow={() => navigate(-1)}
            onDotsClick={() => setIsDropDown(true)}
          />
          {isDropDown && (
            <DropDown>
              <DropDownItem
                onClick={() => {
                  setIsEditing(false);
                  setIsDropDown(false);
                }}>
                Отменить
              </DropDownItem>
              <DropDownItem onClick={deleteThisPortfolio}>Удалить</DropDownItem>
              <DropDownItem
                onClick={() => {
                  setIsEditing(true);
                  setIsDropDown(false);
                }}>
                Редактировать
              </DropDownItem>
            </DropDown>
          )}
          {isEditing ? (
            <input
              name="portfolio_title"
              className="portfolio-page__input"
              value={portfolio.portfolio_title}
              onChange={(e) =>
                setPortfolio((prev) => ({
                  ...prev,
                  [e.target.name]: e.target.value,
                }))
              }
            />
          ) : (
            <h1 className="page__title portfolio-page__title">
              {portfolio.portfolio_title}
            </h1>
          )}
          <div className="portfolio-page-additional">
            <img
              src={preview}
              alt="preview"
              className="portfolio-page__img"></img>

            {isEditing ? (
              <textarea
                name="portfolio_description"
                value={portfolio.portfolio_description}
                onChange={(e) =>
                  setPortfolio((prev) => ({
                    ...prev,
                    [e.target.name]: e.target.value,
                  }))
                }
              />
            ) : (
              <p className="portfolio-page__descrtiption">
                {portfolio.portfolio_description}
              </p>
            )}

            {isEditing && (
              <Button
                className={"portfolio-page__button"}
                text={"сохранить"}
                onClick={savePortfolio}
                style={"white"}
              />
            )}
          </div>
        </div>
      </Layout>
    );
  }
};
