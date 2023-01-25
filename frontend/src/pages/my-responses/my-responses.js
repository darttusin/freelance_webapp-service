import { Layout } from "../../components/Layout/Layot";
import { ResponseCard } from "../../components/Сards/ResponseCard/ResponseCard";
import { useQuery } from "react-query";
import { getMyResponses, getMyOffers } from "../../http/responses";
import toggle from "../../icons/switch1.png";
import "../../styles/responses.css";
import { useState } from "react";
import { AdvertsCard } from "../../components/Сards/AdvertsCard/AdvertsCard";

export const MyResponses = () => {
  const [isToggled, setIsToggled] = useState(true);

  const { data: responses, isLoading: isRespLoading } = useQuery(
    "my-responses",
    getMyResponses
  );
  const {
    data: offers,
    isLoading: isOffersLoading,
    refetch,
  } = useQuery("my-offers", getMyOffers);

  const onToggleClick = () => {
    setIsToggled((prev) => !prev);
  };
  if (isRespLoading || isOffersLoading) {
    return "Loading...";
  }

  return (
    <Layout withFooter={true}>
      <div className="responses">
        <div className="responses-header">
          <p
            className={`title responses-header__title ${
              !isToggled && "responses-header__title_active"
            }`}>
            Мои отклики
          </p>
          <p
            className={`title responses-header__title ${
              isToggled && "responses-header__title_active"
            }`}>
            Мои предложения
          </p>
          <img
            src={toggle}
            onClick={onToggleClick}
            className={"responses-header__img"}
            alt="switch"
          />
        </div>
        {isToggled
          ? responses.items.map((item) => <ResponseCard {...item} />)
          : offers.items.map((item) => (
              <AdvertsCard
                isOffer={true}
                refetch={refetch}
                {...item}
              />
            ))}
      </div>
    </Layout>
  );
};
