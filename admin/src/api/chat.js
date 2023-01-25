import { $api } from ".";

export const getChat = (room) => {
  return $api.get(`admin/chat=${room}`).then((response) => response.data);
};
