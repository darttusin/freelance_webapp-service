import { $api } from ".";

export const newPortfolio = async (data) => {
  return $api.post("/portfolio", data).then((response) => response);
};

export const getPortfolio = async (id) => {
  return $api.get(`/portfolio/${id}`).then((response) => response.data);
};

export const updatePortfolio = async (data) => {
  return $api.put("/portfolio", data);
};

export const deletePortfolio = async (id) => {
  return $api.delete(`/portfolio/${id}`);
};
