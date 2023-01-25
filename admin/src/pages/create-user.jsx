import { MainLayout } from "../Layouts/MainLayout";
import { Button, Form } from "react-bootstrap";
import { useEffect, useRef, useState } from "react";
import { createUser } from "../api/user";
import { Alert } from "react-bootstrap";
import "../styles/user.scss";

export const CreateUser = () => {
  const [lastUser, setLastUser] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [newUser, setNewUser] = useState({
    username: "",
    email: "",
    password: "",
    tg_name: "string",
  });
  const roleRef = useRef();
  const [isDisabled, setIsDisabled] = useState(true);

  const handleCLick = async () => {
    newUser["role"] = roleRef.current.value;
    await createUser(newUser);

    setShowAlert(true);
    setLastUser(newUser.username);
    setNewUser({ username: "", email: "", password: "", tg_name: "string" });

    setTimeout(() => {
      setShowAlert(false);
    }, 3000);
  };

  useEffect(() => {
    setIsDisabled(!newUser.username || !newUser.email || !newUser.password);
  }, [newUser]);

  return (
    <MainLayout page={"Создание пользователя"}>
      {showAlert && (
        <Alert variant={"success"}>
          Пользователь {lastUser} создан успешно
        </Alert>
      )}
      <Form className="user-form">
        <Form.Group className="mb-3">
          <Form.Label>Email</Form.Label>
          <Form.Control
            value={newUser.email}
            onChange={(e) =>
              setNewUser((prev) => ({
                ...prev,
                [e.target.name]: e.target.value,
              }))
            }
            name="email"
            placeholder="Email"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Username</Form.Label>
          <Form.Control
            value={newUser.username}
            onChange={(e) =>
              setNewUser((prev) => ({
                ...prev,
                [e.target.name]: e.target.value,
              }))
            }
            name="username"
            placeholder="username"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            value={newUser.password}
            onChange={(e) =>
              setNewUser((prev) => ({
                ...prev,
                [e.target.name]: e.target.value,
              }))
            }
            name="password"
            placeholder="Password"
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Role</Form.Label>
          <Form.Select
            ref={roleRef}
            name="role">
            <option>admin</option>
            <option>user</option>
            <option>manager</option>
          </Form.Select>
        </Form.Group>
        <Button
          onClick={handleCLick}
          disabled={isDisabled}
          className="user-form__button"
          variant="primary">
          Создать пользователя
        </Button>
      </Form>
    </MainLayout>
  );
};
