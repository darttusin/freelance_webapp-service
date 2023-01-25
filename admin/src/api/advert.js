import { $api } from ".";

export const getAdvert = (id) => {
  return $api.get(`admin/advert=${id}`).then((response) => response.data);
};
