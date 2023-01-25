import { useState } from "react";
import { Button } from "../../components/Button/Button";
import { Layout } from "../../components/Layout/Layot";
import { PageHeader } from "../../components/PageHeader/PageHeader";
import { CustomSelect } from "../../components/Select/Select";
import { scope, cityOptions } from "../../сonstants/constants";
import { createAdvert } from "../../http/adverts";
import "../../styles/create-advert.css";
import { useNavigate } from "react-router-dom";

export const CreateAdvert = () => {
  const [scopeOption, setScopeOption] = useState(scope[0]);
  const [cityOption, setCityOption] = useState(cityOptions[0]);
  const navigate = useNavigate();

  const [advert, setAdvert] = useState({
    advert_text: "",
    advert_title: "",
    advert_category: "",
    advert_city: "",
    advert_price: 1,
  });

  const createNewAdvert = async () => {
    const response = await createAdvert({
      ...advert,
      advert_category: scopeOption.label,
      advert_city: cityOption.label,
    });
    if (response.status == 200) {
      navigate(`/advert/${response.data.advert_id}`);
    }
  };

  return (
    <Layout withFooter={true}>
      <div className="create-advert">
        <PageHeader
          handleArrow={() => navigate(-1)}
          withDots={false}
        />
        <p className="title">Создание объявления</p>
        <p className="adverts-filter__label">Сфера</p>
        <CustomSelect
          selectedOption={scopeOption}
          className={"select"}
          onChange={setScopeOption}
          options={scope}
        />
        <p className="adverts-filter__label">Город</p>
        <CustomSelect
          className={"select"}
          options={cityOptions}
          onChange={setCityOption}
          selectedOption={cityOption}
        />
        <p className="adverts-filter__label">Заголовок</p>
        <input
          type="text"
          name="advert_title"
          onChange={(e) =>
            setAdvert((prev) => ({ ...prev, [e.target.name]: e.target.value }))
          }
          value={advert.advert_title}
          placeholder="Заголовок"
          min="1"></input>
        <p className="adverts-filter__label">Оплата</p>
        <input
          type="number"
          name="advert_price"
          onChange={(e) =>
            setAdvert((prev) => ({
              ...prev,
              [e.target.name]: e.target.value,
            }))
          }
          value={advert.advert_price}
          placeholder="0 Р"
          min="1"
          max="1000000"></input>
        <p className="adverts-filter__label">Описание</p>
        <textarea
          name="advert_text"
          onChange={(e) =>
            setAdvert((prev) => ({ ...prev, [e.target.name]: e.target.value }))
          }
          value={advert.advert_text}></textarea>
        <Button
          onClick={createNewAdvert}
          style={"white"}
          text={"Создать"}
        />
      </div>
    </Layout>
  );
};
