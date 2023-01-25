import { Layout } from "../../components/Layout/Layot";
import { AdvertsCard } from "../../components/Сards/AdvertsCard/AdvertsCard";
import { AdvertsFilter } from "../../components/Filter/AdvertsFilter";
import { Pagination } from "../../components/Pagination/Pagination";
import { useState } from "react";
import { useQuery } from "react-query";
import settings from "../../icons/settings.svg";
import "../../styles/adverts.css";
import { getAdverts } from "../../http/adverts";
import { useLocation, useParams } from "react-router-dom";

export const Adverts = () => {
  const [isFilter, setIsFilter] = useState(false);
  const [city, setCity] = useState("None");
  const [scope, setScope] = useState("None");
  const [adverts, setAdverts] = useState();
  const location = useLocation();
  const page = location?.state?.page ? location.state.page : 1;

  const { isLoading, refetch } = useQuery(
    ["adverts", city, scope, page],
    () => getAdverts(city, scope, page),
    { onSuccess: setAdverts }
  );

  return (
    <Layout withFooter={true}>
      <div className="adverts">
        <div className="adverts-header">
          <p className="title">{isFilter ? "Фильтр" : "Обьявления"}</p>
          <img
            src={settings}
            onClick={() => {
              setIsFilter((prev) => !prev);
            }}
            alt="settings"></img>
        </div>
        {isFilter ? (
          <AdvertsFilter
            city={{ label: city, value: "" }}
            scope={{ label: scope, value: "" }}
            setIsFilter={setIsFilter}
            setCity={setCity}
            setScope={setScope}
            refetch={refetch}
          />
        ) : (
          <>
            {isLoading ? (
              "Loading..."
            ) : (
              <>
                {adverts?.items?.map((advert, index) => (
                  <AdvertsCard
                    key={index}
                    {...advert}
                  />
                ))}
              </>
            )}
          </>
        )}
        {Math.ceil(adverts?.total / adverts?.size) > 1 && (
          <Pagination
            forcePage={adverts?.page - 1}
            pageCount={Math.ceil(adverts?.total / adverts?.size)}
            pageRangeDisplayed={5}
          />
        )}
      </div>
    </Layout>
  );
};
