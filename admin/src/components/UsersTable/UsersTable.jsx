import Table from "react-bootstrap/Table";
import { useNavigate } from "react-router-dom";

const TableRow = ({ user, index }) => {
  const navigate = useNavigate();

  const onRowClick = () => {
    navigate(`./${user.user_id}`);
  };
  return (
    <tr onClick={onRowClick}>
      <td>{index}</td>
      <td>{user.user_name}</td>
      <td>{user.user_email}</td>
      <td>{user.user_id}</td>
    </tr>
  );
};

export const UsersTable = ({ users }) => {
  return (
    <Table
      responsive
      bordered
      hover
      size="lg">
      <thead>
        <tr>
          <th>#</th>
          <th>username</th>
          <th>email</th>
          <th>id</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user, index) => (
          <TableRow
            key={index}
            user={user}
            index={index}
          />
        ))}
      </tbody>
    </Table>
  );
};
