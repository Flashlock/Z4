import { HashRouter, Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./Layout";
import { HomePage } from "./features/home/HomePage";
import { MarketPage } from "./features/market/MarketPage";

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="market" element={<MarketPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}
