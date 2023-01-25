import { $api } from ".";

export const getPerformers = (page) => {
  const raiting = 0;
  const count_jobs = 0;
  const count_reviews = 0;
  return $api
    .get(
      `/performers/params=${raiting}&${count_reviews}&${count_jobs}?page=${page}
  `
    )
    .then((response) => response.data);
};
