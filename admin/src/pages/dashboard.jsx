import { DashCard } from "../components/Cards/DashCard/DashCard";
import { MainLayout } from "../Layouts/MainLayout";

export const DashBoard = () => {
  return (
    <MainLayout page={"Главная"}>
      <div className="dashboard-cards">
        <DashCard
          title={"Количество"}
          amount={100}
        />
        <DashCard
          title={"Количество"}
          amount={100}
        />
        <DashCard
          title={"Количество"}
          amount={100}
        />
        <DashCard
          title={"Количество"}
          amount={100}
        />
      </div>
    </MainLayout>
  );
};
