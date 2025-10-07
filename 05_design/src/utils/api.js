import axios from 'axios';

// Create a custom instance
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

export default api;