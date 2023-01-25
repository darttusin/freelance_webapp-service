import "./JobOffer.css";
import { Button } from "../Button/Button";
import { useQuery } from "react-query";
import { geyMyAdverts, offerJob } from "../../http/adverts";
import { JobOfferCard } from "../Сards/JobOfferCard/JobOfferCard";
import { useState } from "react";

export const JobOffer = ({ toggleOffer, userId }) => {
  const { data, isLoading } = useQuery("job-adverts", geyMyAdverts);
  const [activeIndex, setActinveIndex] = useState(-1);
  const [offer, setOffer] = useState();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const onOfferClick = (advert_id, index) => {
    if (index === activeIndex) {
      setActinveIndex(-1);
      setOffer();
    } else {
      setOffer(advert_id);
      setActinveIndex(index);
    }
  };

  const makeOffer = async () => {
    if (offer) {
      const data = {
        user_id: userId,
        advert_id: offer,
      };
      await offerJob(data);
      toggleOffer();
    }
  };

  return (
    <div className="job">
      <div className="job-header">
        <div className="job-header__title">Выбрать проект</div>
        <div
          className="close-button"
          onClick={toggleOffer}>
          х
        </div>
      </div>
      <div className="job-adverts">
        {data?.map((item, index) => (
          <JobOfferCard
            activeIndex={activeIndex}
            key={index}
            index={index}
            {...item}
            onOfferClick={onOfferClick}
          />
        ))}
      </div>
      <Button
        onClick={makeOffer}
        className={"job-header__button"}
        style="white"
        text="Предложить"
      />
    </div>
  );
};
