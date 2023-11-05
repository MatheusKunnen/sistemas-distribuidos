import React from "react";
import { Routes, Route } from "react-router-dom";
import CreateAccount from "../pages/CreateAccount";
import Login from "../pages/Login";
import Home from "../pages/Home";
import ProductCreate from "../pages/Products/Create";
import ProductMovement from "../pages/Products/Movement";
import ReportsStock from "../pages/Reports/Stock";
import ReportsMovements from "../pages/Reports/Movements";
import ReportsWithoutOutput from "../pages/Reports/WithoutOutput";
// import PrivateRoutes from "./PrivateRoutes";

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<Login />} />
    <Route path="/create-account" element={<CreateAccount />} />
    <Route path="/home" element={<Home />} />
    <Route path="/product/create" element={<ProductCreate />} />
    <Route path="/product/movement" element={<ProductMovement />} />
    <Route path="/reports/stock" element={<ReportsStock />} />
    <Route path="/reports/movements" element={<ReportsMovements />} />
    <Route path="/reports/without-output" element={<ReportsWithoutOutput />} />
  </Routes>
);

export default AppRoutes;
