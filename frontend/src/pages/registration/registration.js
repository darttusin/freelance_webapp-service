import { Button } from "../../components/Button/Button";
import { Input } from "../../components/Input/Input";
import { Layout } from "../../components/Layout/Layot";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { registration, login } from "../../http/user";
import { setCookie } from "../../utils/cookie";
import "../../styles/auth.css";

export const Registration = ({ setToken }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState({
    username: "",
    email: "",
    password: "",
    tg_name: "",
    role: "user",
  });

  const submitForm = async () => {
    try {
      const reg = await registration(user);
      const auth = await login({
        username: user.email,
        password: user.password,
      });
      setCookie("access_token", auth.access_token);
      setToken(auth.access_token);
      navigate("/profile");
    } catch {}
  };
  return (
    <Layout>
      <div className="auth">
        <div className="auth-form">
          <p className="auth__title">Регистрация</p>

          <Input
            label={"name"}
            onChange={(e) => {
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }));
            }}
            name="username"
            placeholder={"Сережа"}></Input>
          <Input
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            label={"tg_name"}
            name="tg_name"
            placeholder={"rengated"}></Input>
          <Input
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            label={"mail"}
            name="email"
            placeholder={"your@mail.ru"}></Input>
          <Input
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            name="password"
            label={"password"}
            type="password"
            placeholder={"******"}></Input>

          <Button
            onClick={submitForm}
            style={"blue"}
            text={"Отправить"}
          />
        </div>
      </div>
    </Layout>
  );
};
