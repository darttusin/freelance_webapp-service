import { useNavigate } from "react-router-dom";
import avatar from "../../../img/avatar.png";
import "./ChatCard.css";

export const ChatCard = ({ user_name, chat_room_id, last_message }) => {
  const navigate = useNavigate();
  return (
    <div
      onClick={() => {
        navigate(`/chat/${chat_room_id}`);
      }}
      className="chat-card">
      <img
        className="chat-card__image"
        src={avatar}
        alt=""
      />
      <div className="chat-card-text">
        <div className="chat-card-header">
          <p className="chat-card__name">{user_name}</p>
          <p className="chat-card__time">вт</p>
        </div>
        <p className="chat-card-text_lastmessage">{last_message}</p>
      </div>
    </div>
  );
};
