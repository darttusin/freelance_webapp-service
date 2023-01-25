import "../styles/chat.scss";
import { MessageBox, MessageList } from "react-chat-elements";
import { getChat } from "../api/chat";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import { MainLayout } from "../Layouts/MainLayout";

export const Chat = ({}) => {
  const { name, id } = useParams();

  const { data, isLoading } = useQuery(["messages", id], () => getChat(id));
  if (isLoading) {
    return <MainLayout page={"Чаты"}></MainLayout>;
  }

  return (
    <MainLayout page={data[0].advert_title}>
      <div className="chat">
        {data[1].map((message) => (
          <MessageBox
            width={"50%"}
            title={message.user_name}
            position={message.user_name == name ? "left" : "right"}
            type={"text"}
            text={message.message_text}
            date={message.message_time}
          />
        ))}
      </div>
    </MainLayout>
  );
};
