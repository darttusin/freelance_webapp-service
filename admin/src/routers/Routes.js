import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { DashBoard } from "../pages/dashboard";
import { Login } from "../pages/login";
import { Users } from "../pages/users";
import { User } from "../pages/user";
import { CreateUser } from "../pages/create-user";
import { NotFound } from "../pages/not-found";
import { Advert } from "../pages/advert";
import { useEffect, useState } from "react";
import { getCookie } from "../utils/cookie";
import { Chat } from "../pages/chat";

export const MainRoutes = () => {
  const [token, setToken] = useState(getCookie("token"));

  useEffect(() => {
    setToken(getCookie("token"));
  }, [window.location.pathname]);

  return (
    <Router>
      <Routes>
        <Route
          path="*"
          element={<NotFound />}
        />
        <Route
          path="chat/:name/:id"
          element={token ? <Chat /> : <Navigate to="/login" />}
        />
        <Route
          path="advert/:id"
          element={token ? <Advert /> : <Navigate to="/login" />}
        />
        <Route
          path="/login"
          element={!token ? <Login setToken={setToken} /> : <Navigate to="/" />}
        />
        <Route
          path="/"
          element={token ? <Navigate to="/users" /> : <Navigate to="/login" />}
        />
        <Route
          path="users/:id"
          element={token ? <User /> : <Navigate to="/login" />}
        />
        <Route
          path="users"
          element={token ? <Users /> : <Navigate to="/login" />}
        />
        <Route
          path="/create-user"
          element={token ? <CreateUser /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
};
