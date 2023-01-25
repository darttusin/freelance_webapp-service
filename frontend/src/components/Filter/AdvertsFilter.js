import { useState } from "react";
import { Button } from "../Button/Button";
import { CustomSelect } from "../Select/Select";
import { OptionalFilters } from "./OptionalFilters";
import plus from "../../icons/plus.svg";
import minus from "../../icons/minus.svg";
import { cityOptions, scope as scopeOptions } from "../../сonstants/constants";
import "./Filter.css";

export const AdvertsFilter = ({
  setScope,
  setCity,
  city,
  scope,
  setIsFilter,
  refetch,
}) => {
  const [optionalFilters, setOptionalFilters] = useState({
    city: { active: true, options: cityOptions },
  });
  const [selectedcity, setSelectedcity] = useState(city);
  const [selectedScope, setSelectedScope] = useState(scope);

  const onSumbit = () => {
    setCity(selectedcity.label);
    setScope(selectedScope.label);
    setIsFilter(false);
    refetch();
  };

  return (
    <div className="adverts-filter">
      <p className="adverts-filter__label">Сфера</p>
      <CustomSelect
        className={"select"}
        selectedOption={selectedScope}
        onChange={setSelectedScope}
        options={scopeOptions}
      />
      <OptionalFilters
        optionalFilters={optionalFilters}
        setOptionalFilters={setOptionalFilters}
      />
      {Object.keys(optionalFilters).map((key, index) => (
        <>
          {optionalFilters[key].active && (
            <div key={index}>
              <div className="adverts-filter-optional__header">
                <p className="adverts-filter__label">{key}</p>
                <img
                  alt=""
                  src={minus}
                  onClick={() =>
                    setOptionalFilters((prev) => ({
                      ...prev,
                      [key]: {
                        active: false,
                        options: optionalFilters[key].options,
                      },
                    }))
                  }
                />
              </div>
              <CustomSelect
                key={index}
                className={"select"}
                selectedOption={eval(`selected${key}`)}
                onChange={eval(`setSelected${key}`)}
                options={optionalFilters[key].options}
              />
            </div>
          )}
        </>
      ))}

      <Button
        className="adverts__button"
        onClick={onSumbit}
        style="white"
        text={"применить"}
      />
    </div>
  );
};
