import { Button } from "../Button/Button";
import { PageHeader } from "../PageHeader/PageHeader";
import "./ModalResponse.css";
import avatar from "../../img/avatar.png";
import { updateResponse } from "../../http/adverts";

export const ModalResponse = ({
  user_name,
  user_id,
  advert_id,
  response_price,
  response_text,
  setModalResponse,
  refetch,
}) => {
  const handleArrow = () => {
    setModalResponse((prev) => ({ ...prev, show: false }));
  };

  const onSetCustomer = async () => {
    const data = {
      user_id: user_id,
      advert_id: advert_id,
      response_status: "4",
    };

    await updateResponse(data);
    setModalResponse((prev) => ({ ...prev, show: false }));
    refetch();
  };
  return (
    <div className="modal-response-wrapper">
      <div className="modal-response-content">
        <PageHeader
          handleArrow={handleArrow}
          withDots={false}
        />
        <div>
          <div className="modal-response-body">
            <img
              src={avatar}
              className="modal-response__image"
            />
            <div className="modal-response-text">
              <p className="modal-response-text__item">{user_name}</p>
              <p className="modal-response-text__item">{response_text}</p>
              <div></div>
            </div>
          </div>
        </div>
        <div className="modal-response-footer">
          <Button
            onClick={onSetCustomer}
            className="modal-response-footer__button"
            style="black"
            text={"Назначить исполнителем"}></Button>
          <p className="modal-response__price">{response_price}</p>
        </div>
      </div>
    </div>
  );
};
