import { MainLayout } from "../Layouts/MainLayout";
import { Table } from "react-bootstrap";
import { UsersTable } from "../components/UsersTable/UsersTable";
import { useQuery } from "react-query";
import { getUsers } from "../api/user";
import { Spinner } from "react-bootstrap";
import "../styles/users.scss";

export const Users = () => {
  const { data, isLoading } = useQuery("all-users", getUsers);

  if (isLoading) {
    return (
      <MainLayout page={"Пользователь"}>
        <Spinner />
      </MainLayout>
    );
  }
  return (
    <MainLayout page={"Пользователи"}>
      <div className="users">
        <div className="users-header">
          <p className="users__title">Все пользователи</p>
          <div className="users-sorting">
            {/* <p className="users-sorting__item"></p> */}
            {/* <p className="users-sorting__item"></p> */}
          </div>
        </div>
        {!isLoading && <UsersTable users={data?.items} />}
      </div>
    </MainLayout>
  );
};
