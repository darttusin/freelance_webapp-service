import { useState } from "react";
import { useQuery } from "react-query";
import { Filter } from "../../components/Filter/AdvertsFilter";
import { Layout } from "../../components/Layout/Layot";
import { PerformersCard } from "../../components/Сards/PerformersCard/PerformersCard";
import { getPerformers } from "../../http/performers";
import { Pagination } from "../../components/Pagination/Pagination";
import settings from "../../icons/settings.svg";
import "../../styles/perfomers.css";
import { useLocation } from "react-router-dom";

export const Performers = () => {
  const [isFilter, setIsFilter] = useState(false);
  const location = useLocation();
  const page = location?.state?.page ? location.state.page : 1;
  const { data, isLoading } = useQuery(["performers", page], () =>
    getPerformers(page)
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Layout withFooter={true}>
      <div className="perfomers">
        <div className="perfomers-header">
          <p className="title">{!isFilter ? "Исполнители" : "Фильтр"}</p>
          <img
            className="settings"
            src={settings}
            onClick={() => {
              setIsFilter((prev) => !prev);
            }}
            alt="settings"></img>
        </div>
        {isFilter ? (
          // <Filter />
          ""
        ) : (
          <>
            {data?.items?.map((performer) => (
              <PerformersCard {...performer} />
            ))}
          </>
        )}
        {Math.ceil(data?.total / data?.size) > 1 && (
          <Pagination
            forcePage={data?.page - 1}
            pageCount={Math.ceil(data?.total / data?.size)}
            pageRangeDisplayed={5}
          />
        )}
      </div>
    </Layout>
  );
};
