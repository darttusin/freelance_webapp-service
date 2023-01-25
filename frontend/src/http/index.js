import axios from "axios";
import { getCookie, setCookie } from "../utils/cookie";

export const $api = axios.create({
  // baseURL: "https://fwbot.ru/backend/",
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
  },
});

$api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${getCookie("access_token")}`;
  return config;
});

$api.interceptors.response.use(
  function (response) {
    // Do something with response data
    return response;
  },
  function (error) {
    if (error.response.status == 401) {
      setCookie("access_token", "");
      localStorage.setItem("id", "");
      window.location.replace("/login");
    }
    return Promise.reject(error);
  }
);
