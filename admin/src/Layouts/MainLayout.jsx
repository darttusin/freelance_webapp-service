import { Header } from "../components/Header/Header";
import { SideBar } from "../components/SideBar/SideBar";
import "./mainlayout.scss";

export const MainLayout = ({ children, page }) => {
  return (
    <main className="main">
      <SideBar />
      <div className="main-content">
        <Header page={page} />
        <div>{children}</div>
      </div>
    </main>
  );
};
