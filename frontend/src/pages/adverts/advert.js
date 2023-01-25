import { useEffect, useState } from "react";
import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import { AdvertResponse } from "../../components/AdvertResponse/AdvertResponse";
import { Button } from "../../components/Button/Button";
import { DropDown, DropDownItem } from "../../components/DropDown/DropDown";
import { Layout } from "../../components/Layout/Layot";
import { ModalResponse } from "../../components/ModalResponse/ModalResponse";
import { PageHeader } from "../../components/PageHeader/PageHeader";
import { getAdvert } from "../../http/adverts";
import { createResponse } from "../../http/responses";
import { deleteAdvert as deleteAd } from "../../http/adverts";
import { ChatCard } from "../../components/Сards/СhatCard/ChatCard";
import "../../styles/adverts.css";

export const Advert = () => {
  const navigate = useNavigate();
  const [showDropDrown, setShowDropDown] = useState(false);
  const [modalResponse, setModalResponse] = useState({
    user_id: "",
    show: false,
    user_name: "",
    response_price: "",
    response_text: "",
  });

  const my_id = localStorage.getItem("id");
  const { id } = useParams();
  const [advert, setAdvert] = useState();
  const [data, setData] = useState({
    advert_id: id,
    responce_text: "",
    price: 0,
  });

  const mode = localStorage.getItem("mode");
  const { isLoading, refetch } = useQuery(["advert", id], () => getAdvert(id), {
    onSuccess: setAdvert,
  });

  const [isResponse, setIsResponse] = useState(false);

  useEffect(() => {
    advert?.responces?.forEach((element) => {
      if (element.user_id === my_id) {
        setIsResponse(true);
      }
    });
  }, [advert]);

  const newResponse = async () => {
    await createResponse(data);
    refetch();
  };

  const toggleDropDown = () => {
    setShowDropDown((prev) => !prev);
  };

  const deleteAdvert = async () => {
    await deleteAd(id);
    navigate("/my-adverts");
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (mode !== "customer") {
    return (
      <Layout withFooter={true}>
        <div className="adverts">
          <PageHeader handleArrow={() => navigate(-1)} />
          <div className="advert-text">
            <p className="advert__title">{advert?.advert.advert_title}</p>
            <p className="advert__price">{advert?.advert.advert_price}</p>
          </div>

          <p className="advert__description">{advert?.advert.advert_text}</p>
          {!isResponse ? (
            <>
              <textarea
                name="responce_text"
                onChange={(e) =>
                  setData((prev) => ({
                    ...prev,
                    [e.target.name]: e.target.value,
                  }))
                }
                placeholder="я смогу выполнить эту работу за 3 дня"
              />
              <div className="advert-bottom">
                <input
                  type="number"
                  min="0"
                  className="advert-input"
                  name="price"
                  value={advert?.price}
                  placeholder="0 Р"
                  onChange={(e) =>
                    setData((prev) => ({
                      ...prev,
                      [e.target.name]: e.target.value,
                    }))
                  }
                />
                <Button
                  style="black"
                  onClick={newResponse}
                  text="откликнуться"
                />
              </div>
            </>
          ) : (
            <>{advert?.chats.length > 0 && <ChatCard {...advert.chats[0]} />}</>
          )}
        </div>
      </Layout>
    );
  } else {
    return (
      <>
        <Layout withFooter={true}>
          {modalResponse.show && (
            <ModalResponse
              refetch={refetch}
              advert_id={id}
              {...modalResponse}
              setModalResponse={setModalResponse}
            />
          )}
          <div className="adverts">
            <PageHeader
              handleArrow={() => navigate(-1)}
              onDotsClick={toggleDropDown}
            />
            {showDropDrown && (
              <DropDown>
                <DropDownItem onClick={toggleDropDown}>Отменить</DropDownItem>
                <DropDownItem onClick={deleteAdvert}>
                  Удалить объявление
                </DropDownItem>
              </DropDown>
            )}

            <div className="advert-text">
              <p className="advert__title">{advert?.advert.advert_title}</p>
              <p className="advert__price">{advert?.advert.advert_price} Р</p>
            </div>
            <p className="advert__description">{advert?.advert.advert_text}</p>
          </div>
          <p className="responses-text">Отклики</p>
          <div>
            {advert?.responces?.map((item) => (
              <AdvertResponse
                setModalResponse={setModalResponse}
                {...item}
              />
            ))}
          </div>
        </Layout>
      </>
    );
  }
};
