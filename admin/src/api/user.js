import { $api } from "./index";

export const login = async (user) => {
  return $api
    .post("/admin/login", user, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    })
    .then((response) => response.data);
};

export const getUsers = async () => {
  return $api.get("/admin/users").then((response) => response.data);
};

export const getUser = async (id) => {
  return $api.get(`/admin/user=${id}`).then((response) => response.data);
};

export const createUser = async (user) => {
  $api.post("/registration", user, {
    headers: { "Content-Type": "application/json" },
  });
};
