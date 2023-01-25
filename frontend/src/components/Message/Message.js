import avatar from "../../img/avatar.png";

export const Message = ({ message_text, user_id, currentUser, position }) => {
  return (
    <div
      className={`chat-message ${
        currentUser === user_id ? "chat-message_left" : "chat-message_right"
      }`}>
      <img
        src={avatar}
        alt=""></img>
      <p>{message_text}</p>
    </div>
  );
};
