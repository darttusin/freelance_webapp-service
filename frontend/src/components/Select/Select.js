import React from "react";

import Select from "react-select";

export const CustomSelect = ({
  options,
  selectedOption,
  className,
  onChange,
}) => (
  <div className={className}>
    <Select
      value={selectedOption}
      onChange={onChange}
      defaultValue={options[0]}
      options={options}
      theme={(theme) => ({
        ...theme,
        borderRadius: 5,
        colors: {
          ...theme.colors,
          primary25: "#F2F3F5",
          primary: "black",
        },
      })}
    />
  </div>
);
