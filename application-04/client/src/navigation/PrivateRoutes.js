import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/auth";

const PrivateRoutes = () => {
  const { token, signOut } = useAuth();

  const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split(".")[1]));
    } catch (e) {
      return null;
    }
  };

  if (token) {
    const decodedJwt = parseJwt(token);
    if (decodedJwt.exp * 1000 < Date.now()) {
      console.log("User logged out because the token expired");
      signOut();
    }
  }

  return !!token ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoutes;
