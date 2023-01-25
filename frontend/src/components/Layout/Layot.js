import { Footer } from "../Footer/Footer";
import { Header } from "../Header/Header";

export const Layout = ({ children, withFooter }) => {
  return (
    <>
      <Header></Header>
      <main className={`main`}>{children}</main>
      {withFooter && <Footer />}
    </>
  );
};
