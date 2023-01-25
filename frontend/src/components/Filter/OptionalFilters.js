import plus from "../../icons/plus.svg";

export const OptionalFilters = ({ optionalFilters, setOptionalFilters }) => {
  const keys = Object.keys(optionalFilters);

  return (
    <>
      {keys.map((key, index) => (
        <>
          {!optionalFilters[key].active && (
            <div key={index} className="adverts-filter-opntional">
              <p>{key}</p>
              <img
                onClick={(e) =>
                  setOptionalFilters((prev) => ({
                    ...prev,
                    [key]: {
                      active: true,
                      options: optionalFilters[key].options,
                    },
                  }))
                }
                alt=""
                src={plus}
              />
            </div>
          )}
        </>
      ))}
    </>
  );
};
