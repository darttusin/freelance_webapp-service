import { useNavigate } from "react-router-dom";
import avatar from "../../../images/avatar.png";
import "./ChatCard.scss";

export const ChatCard = ({ user_name, chat_room_id, last_message, index }) => {
  const navigate = useNavigate();

  const onChatClick = () => {
    navigate(`/chat/${user_name}/${chat_room_id}`);
  };
  return (
    <div
      onClick={onChatClick}
      className="chat-card">
      <img
        src={avatar}
        className="chat-card__image"
        alt="chat"
      />

      <div className="chat-card-text">
        <p className="chat-card__title">{user_name}</p>
        <p className="chat-card__lastmessage">{last_message}</p>
      </div>
    </div>
  );
};
