import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Header } from "../../components/Header/Header";
import { Message } from "../../components/Message/Message";
import { getChat } from "../../http/chat";
import { ModalResponse } from "../../components/ModalResponse/ModalResponse";
import { ModalReview } from "../../components/ModalReview/ModalReview";
import { unlockChat } from "../../http/chat";
import clip from "../../icons/clip.svg";
import send from "../../icons/send-arrow.svg";
import avatar from "../../img/avatar.png";
import arrowBack from "../../icons/back-arrow.svg";

const currentUser = localStorage.getItem("id");

export const SingleChat = () => {
  const [modalResponse, setModalReponse] = useState({
    show: false,
  });

  const [modalReview, setModalReview] = useState({ show: false });

  const mode = localStorage.getItem("mode");
  const navigate = useNavigate();
  const ws = useRef();

  const [chat, setChat] = useState();
  const { roomId } = useParams();
  const [currentMessage, setCurrentMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const onUnlockClick = async () => {
    await unlockChat(roomId);
    setChat((prev) => ({ ...prev, chat_opened: true }));
  };

  const onSubHeaderClick = (advert_id) => {
    navigate(`/advert/${advert_id}`);
  };

  const onSetPerformer = async () => {
    setModalReponse((prev) => ({ ...prev, show: true }));
  };

  const onCloseCase = () => {
    setModalReview((prev) => ({ ...prev, show: true }));
  };

  useEffect(() => {
    // ws.current = new WebSocket(`wss://fwbot.ru/websocket/${roomId}`);
    ws.current = new WebSocket(`ws://localhost:8000/ws/${roomId}`);

    // Opening the ws connection

    ws.current.onopen = async () => {
      const messages = await getChat(roomId);
      setChat(messages[0]);
      setMessages(messages[1]);
      console.log("Connection opened");
    };

    // Listening on ws new added messages

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };

    return () => {
      console.log("Cleaning up...");
      ws.current.close();
    };
  }, []);

  const sendMessage = () => {
    if (currentMessage != "") {
      var message_obj = {
        message_text: currentMessage,
        user_id: currentUser,
      };
      if (chat && chat.chat_opened) {
        ws.current.send(JSON.stringify(message_obj));
        setCurrentMessage("");
      }

      // setMessages((prev) => [
      //  ...prev,
      //  { message_id: "", user_id: currentUser, message_text: currentMessage },
      //]);
    }
  };

  console.log(
    mode == "peformer" &&
    chat &&
    chat.chat_opened &&
    chat.response_status === "in working" &&
    "Вы назначены исполнителем"
  );

  return (
    <>
      {modalReview.show && (
        <ModalReview
          advert_id={chat.advert_id}
          setModalReview={setModalReview}
          user_id={chat.user_id}
        />
      )}
      {modalResponse.show && (
        <ModalResponse
          advert_id={chat.advert_id}
          user_id={chat.user_id}
          response_text={chat.response_text}
          response_price={chat.response_price}
          setModalResponse={setModalReponse}
          user_name={chat.user_name}
        />
      )}
      <Header />
      <div className="single-chat">
        <div className="chat-header">
          <img
            onClick={() => {
              navigate(-1);
            }}
            src={arrowBack}
            class="arrow-back"
            alt="goback"
          />

          {mode != "customer" &&
            chat &&
            chat.chat_opened &&
            chat.response_status === "in working" && (
              <span className="chat-header__performer">
                "Вы назначены исполнителем"
              </span>
            )}

          {mode == "customer" && chat && !chat.chat_opened ? (
            <button
              onClick={onUnlockClick}
              className="chat-header__unlock-btn">
              Разблокировать чат
            </button>
          ) : (
            <>
              {chat && !chat?.chat_opened && (
                <p className="chat-header__title-locked">Чат заблокирован</p>
              )}
            </>
          )}

          <img
            src={avatar}
            alt=""></img>
          <p>{chat ? chat.user_name : ""}</p>
          {mode == "customer" &&
            chat &&
            chat.chat_opened &&
            chat.response_status != "in working" &&
            chat.response_status != "work finished" && (
              <button
                onClick={onSetPerformer}
                className="chat-header_set-button">
                Назначить исполнителем
              </button>
            )}

          {mode == "customer" &&
            chat &&
            chat.chat_opened &&
            chat.response_status == "in working" && (
              <button
                onClick={onCloseCase}
                className="chat-header_set-button">
                Завершить сделку
              </button>
            )}
        </div>

        {chat && (
          <div
            onClick={() => onSubHeaderClick(chat.advert_id)}
            className="chat-subheader">
            <p>Обьявление: {chat.advert_title}</p>
          </div>
        )}
        <div className="chat-body">
          {messages?.map((message, index) => (
            <Message
              currentUser={currentUser}
              user_id={message.user_id}
              key={index}
              {...message}
            />
          ))}
        </div>
        <div className="chat-footer">
          <img
            src={clip}
            alt="приложить"
            className="chat__image"></img>
          <input
            className="chat-input"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            type="text"
            placeholder="Введите сообщение"
          />
          <img
            src={send}
            alt="отпроавить"
            className="chat__image"
            onClick={sendMessage}></img>
        </div>
      </div>
    </>
  );
};
