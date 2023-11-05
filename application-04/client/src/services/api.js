import axios from "axios";

const api = axios.create({
  baseURL: 'http://localhost:5000/', // local server
});

export default api;
