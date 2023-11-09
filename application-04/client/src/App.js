import * as React from 'react';

import { BrowserRouter } from "react-router-dom";
import AppRoutes from './navigation/AppRoutes';

export default function App() {
  const eventSource = new EventSource("http://localhost:5000/events");
  eventSource.addEventListener("publish", function(event) {
    var data = JSON.parse(event.data);
    console.log("The server says " + data.message);
  })

  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
