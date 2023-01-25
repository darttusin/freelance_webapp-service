import "../styles/login.scss";
import { Button, Form } from "react-bootstrap";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/user";
import { setCookie } from "../utils/cookie";

export const Login = ({ setToken }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState({ username: "", password: "" });

  const onLoginClick = async () => {
    if (user.username && user.password) {
      try {
        const response = await login(user);
        const token = response.access_token;
        localStorage.setItem("name", response.admin_info.admin_login);
        setCookie("token", token);
        setToken(token);
        navigate("/users");
      } catch (e) {}
    }
  };
  return (
    <div className="login-wrapper">
      <div className="login-form">
        <h1 className="login-form__title">Вход в админ панель</h1>
        <p className="login-form__subtitle">Введите почту и пароль ниже</p>
        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            name="username"
            type="email"
            placeholder="Enter email"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            onChange={(e) =>
              setUser((prev) => ({ ...prev, [e.target.name]: e.target.value }))
            }
            name="password"
            type="password"
            placeholder="Enter password"
          />
        </Form.Group>
        <Button
          onClick={onLoginClick}
          variant="primary">
          Войти
        </Button>
      </div>
    </div>
  );
};
