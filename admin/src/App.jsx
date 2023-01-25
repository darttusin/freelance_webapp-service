import "bootstrap/dist/css/bootstrap.min.css";
import "react-chat-elements/dist/main.css";
import "./App.css";
import { MainRoutes } from "./routers/Routes";
import { QueryClient, QueryClientProvider } from "react-query";

function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <MainRoutes />
      </div>
    </QueryClientProvider>
  );
}

export default App;
