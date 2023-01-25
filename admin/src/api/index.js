import axios from "axios";
import { getCookie, setCookie } from "../utils/cookie";

export const $api = axios.create({
  baseURL: "https://localhost:8000",
  headers: {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
  },
});

$api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${getCookie("token")}`;
  return config;
});

$api.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.response.status === 401) {
      setCookie("token", "");
      window.location.replace("/login");
    }
    return Promise.reject(error);
  }
);
