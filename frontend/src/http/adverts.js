import { $api } from ".";

export const geyMyAdverts = async () => {
  return $api.get("/myAdverts").then((response) => response.data);
};

export const createAdvert = async (data) => {
  return $api.post("/advert", data);
};

export const getAdvert = async (id) => {
  return $api.get(`/advert/${id}`).then((response) => response.data);
};

export const getAdverts = (city, category, page) => {
  return $api
    .get(`/adverts/params=${category}&${city}?page=${page}`)
    .then((response) => response.data);
};

export const deleteAdvert = (id) => {
  return $api
    .delete(
      `/advert/${id}
  `
    )
    .then((response) => response);
};

export const offerJob = (data) => {
  return $api.post("/jobOffering", data).then((response) => response.data);
};

export const updateResponse = (data) => {
  return $api.put(`/statusResponce`, data).then((response) => response);
};

export const deleteOffer = (data) => {
  return $api.put("/statusOffer", data).then((response) => response.data);
};

export const finishWork = (id) => {
  return $api.put(`finishWork/${id}`).then((response) => response);
};
