import { $api } from ".";

export const addReview = async (data) => {
  return $api.post("/review", data).then((response) => response);
};

export const getReview = async (id) => {
  return $api.get(`/review/${id}`).then((response) => response.data[0]);
};
