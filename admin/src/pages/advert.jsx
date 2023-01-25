import { MainLayout } from "../Layouts/MainLayout";
import { useParams } from "react-router-dom";
import { useQuery } from "react-query";
import { Spinner } from "react-bootstrap";
import { getAdvert } from "../api/advert";
import "../styles/advert.scss";
import { ResponseCard } from "../components/Cards/ResponseCard/ResponseCard";
import { ChatCard } from "../components/Cards/ChatCard/ChatCard";

export const Advert = () => {
  const { id } = useParams();
  const { data, isLoading } = useQuery(["advert", id], () => getAdvert(id));

  if (isLoading) {
    return (
      <MainLayout page={"Объявление"}>
        <Spinner />
      </MainLayout>
    );
  }

  return (
    <MainLayout page={data.advert_info[0].advert_title}>
      <div className="advert">
        <p className="advert__description">{data.advert_info[0].advert_text}</p>
        <div className="advert-responses">
          <p className="advert__title">Отклики</p>
          <div className="advert-responses-items">
            {data.responces.map((response) => (
              <ResponseCard {...response} />
            ))}
          </div>
        </div>
        <div className="advert-chats">
          <p className="advert__title">Чаты</p>
          <div className="advert-chats-items">
            {data.chats.length ? (
              data.chats.map((chat, index) => (
                <ChatCard
                  index={index}
                  {...chat}
                />
              ))
            ) : (
              <p style={{ color: "white", marginLeft: "5px" }}>
                У этого объявления чатов нет
              </p>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};
