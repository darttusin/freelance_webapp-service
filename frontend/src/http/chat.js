import { $api } from ".";

export const getChats = async (mode) => {
  return $api.get(`/chats/mode=${mode}`).then((response) => response.data);
};

export const createChat = async (data) => {
  return $api.post("/chat", data);
};

export const getChat = async (id) => {
  return $api.get(`/chat/${id}`).then((response) => response.data);
};

export const unlockChat = async (roomId) => {
  return $api.put(`/openChat=${roomId}`).then((response) => response);
};
