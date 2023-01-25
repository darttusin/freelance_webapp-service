import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";

import { QueryClientProvider, QueryClient } from "react-query";

import {
  Login,
  Registration,
  Chat,
  Performers,
  MyResponses,
  MyAdverts,
  Adverts,
  Profile,
  PortfolioPage,
  CreateAdvert,
  CreatePortfolio,
  Review,
  Main,
  Advert,
  SingleChat,
  UserProfile,
} from "./pages/index";

import "./App.css";
import { useState } from "react";
import { getCookie } from "./utils/cookie";

const queryClient = new QueryClient();

export default function App() {
  const { pathname } = useLocation();

  const [token, setToken] = useState(getCookie("access_token"));
  return (
    <QueryClientProvider client={queryClient}>
      <div className="wrapper">
        <div className="content">
          <Routes>
            <Route
              path="/"
              element={<Main />}
            />

            <Route
              path="/login"
              element={
                !token ? (
                  <Login setToken={setToken} />
                ) : (
                  <Navigate to="/profile" />
                )
              }
            />
            <Route
              path="/registration"
              element={
                !token ? (
                  <Registration setToken={setToken} />
                ) : (
                  <Navigate to="/profile" />
                )
              }
            />
            <Route
              path="/adverts"
              element={
                token ? (
                  <Adverts />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/chat"
              element={
                token ? (
                  <Chat />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/chat/:roomId"
              element={
                token ? (
                  <SingleChat />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/my-responses"
              element={
                token ? (
                  <MyResponses />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/my-adverts"
              element={
                token ? (
                  <MyAdverts />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/my-adverts/create-advert"
              element={
                token ? (
                  <CreateAdvert />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/performers"
              element={
                token ? (
                  <Performers />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />

            <Route
              path="/profile"
              element={
                token ? (
                  <Profile setToken={setToken} />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="portfolio/:id"
              element={
                token ? (
                  <PortfolioPage />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/advert/:id"
              element={
                token ? (
                  <Advert />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/profile/create-portfolio"
              element={
                token ? (
                  <CreatePortfolio />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/profile/:userId"
              element={
                token ? (
                  <UserProfile />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
            <Route
              path="/review/:id"
              element={
                token ? (
                  <Review />
                ) : (
                  <Navigate
                    to="/login"
                    state={{ from: pathname }}
                    replace
                  />
                )
              }
            />
          </Routes>
        </div>
      </div>
    </QueryClientProvider>
  );
}
