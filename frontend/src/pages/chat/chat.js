import { useEffect, useState } from "react";
import { useQuery } from "react-query";
import { Layout } from "../../components/Layout/Layot";
import { ChatCard } from "../../components/Сards/СhatCard/ChatCard";
import { getChats } from "../../http/chat";
import "../../styles/chat.css";

export const Chat = () => {
  const mode = localStorage.getItem("mode");
  const { data, isLoading } = useQuery(["chats", mode], () => getChats(mode));
  const [type, setType] = useState(0);
  useEffect(() => {
    const mode = localStorage.getItem("mode");
    mode == "customer" ? setType(0) : setType(1);
  }, []);
  return (
    <Layout withFooter={true}>
      <div className="chat">
        <p className="title chat__title">Чаты</p>
        <div className="chats">
          {data?.map((chat) => (
            <ChatCard {...chat} />
          ))}
        </div>
      </div>
    </Layout>
  );
};
