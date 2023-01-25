import ReactPaginate from "react-paginate";
import { useLocation, useNavigate } from "react-router-dom";
import "./Pagination.css";

export const Pagination = ({ pageCount, pageRangeDisplayed, forcePage }) => {
  console.log(forcePage);
  const location = useLocation();
  const navigate = useNavigate();

  const onPageChange = (event) => {
    navigate(location.pathname, { state: { page: event.selected + 1 } });
  };
  return (
    <ReactPaginate
      forcePage={forcePage}
      onPageChange={onPageChange}
      pageCount={pageCount}
      pageRangeDisplayed={pageRangeDisplayed}
      activeLinkClassName="pagination__link_active"
      containerClassName="pagination-container"
    />
  );
};
