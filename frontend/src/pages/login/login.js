import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Button } from "../../components/Button/Button";
import { Input } from "../../components/Input/Input";
import { Layout } from "../../components/Layout/Layot";
import { useState } from "react";
import "../../styles/auth.css";
import { login } from "../../http/user";
import { setCookie } from "../../utils/cookie";

export const Login = ({ setToken }) => {
  const [user, setUser] = useState({ username: "", password: "" });
  const from = useLocation()?.state?.from;

  const submitForm = async () => {
    try {
      const response = await login(user);
      setCookie("access_token", response.access_token);
      setToken(response.access_token);
      !from ? navigate("/profile") : navigate(from);
    } catch (e) {}
  };

  const navigate = useNavigate();

  return (
    <Layout>
      <div className="auth">
        <div className="auth-form">
          <p className="auth__title">Вход</p>
          <Input
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            label={"login"}
            name="username"
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
            text={"Войти"}
          />
        </div>
      </div>
    </Layout>
  );
};
