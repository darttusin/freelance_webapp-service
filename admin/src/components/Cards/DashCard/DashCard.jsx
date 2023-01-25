import "./Dashcard.scss";

export const DashCard = ({ title, amount }) => {
  return (
    <div className="dashcard">
      <p className="dashcard__title">{title}</p>
      <p className="dashcard__amount">{amount}</p>
    </div>
  );
};
