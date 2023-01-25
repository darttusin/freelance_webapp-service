import Cookies from "universal-cookie";

const cookies = new Cookies();

const getCookie = (key) => cookies.get(key);
const setCookie = (key, value) => {
  cookies.set(key, value, { path: "/" });
};

export { getCookie, setCookie };
