import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/', // local server
});

export default api;
