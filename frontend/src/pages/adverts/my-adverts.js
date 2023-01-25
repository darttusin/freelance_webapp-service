import { useNavigate } from "react-router-dom";
import { Layout } from "../../components/Layout/Layot";
import { MyAdvertsCard } from "../../components/Сards/MyAdvertsCard/MyAdvertsCard";
import { useQuery } from "react-query";
import { geyMyAdverts } from "../../http/adverts";
import plus from "../../icons/plus.svg";
import { useState } from "react";

export const MyAdverts = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useQuery("my-adverts", geyMyAdverts);

  if (isLoading) {
    return "Loading ...";
  }

  if (data) {
    return (
      <Layout withFooter={true}>
        <div className="adverts">
          <div className="adverts-header">
            <p className="title">Мои объявления</p>
            <img
              src={plus}
              alt=""
              onClick={() => navigate("./create-advert")}
            />
          </div>
          {data?.map((item, index) => (
            <MyAdvertsCard
              key={index}
              {...item}
            />
          ))}
        </div>
      </Layout>
    );
  }
};
