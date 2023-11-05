import * as React from 'react';

import { BrowserRouter } from "react-router-dom";
import AppRoutes from './navigation/AppRoutes';

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
