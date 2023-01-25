import { $api } from ".";

export const getMyResponses = async () => {
  return $api.get("/myResponces").then((response) => response.data);
};

export const createResponse = async (data) => {
  return $api.post("/responce", data).then((response) => response);
};

export const getMyOffers = async () => {
  return $api.get("/offers").then((response) => response.data);
};
