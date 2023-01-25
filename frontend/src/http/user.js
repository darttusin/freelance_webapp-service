import { $api } from ".";

export const registration = async (user) => {
  $api.post("/registration", user, {
    headers: { "Content-Type": "application/json" },
  });
};

export const login = async (user) => {
  return $api
    .post(
      "/login",
      {
        ...user,
        grant_type: "",
        scope: "",
        client_id: "",
        client_secret: "",
      },
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    )
    .then((response) => response.data);
};

export const getMyProfile = async () => {
  return $api.get("/cabinet").then((response) => response.data);
};

export const changeProfile = async (data) => {
  return $api.put("/profile", data);
};

export const getProfile = async (id) => {
  return $api.get(`/profile/${id}`).then((response) => response.data);
};
