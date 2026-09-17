import axios from "axios";

// Set REACT_APP_API_URL when building for production (e.g. your deployed
// backend URL). Defaults to the local FastAPI dev server.
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const predictHousePrice = (features) => api.post("/api/predict", features);
export const getHistory = () => api.get("/api/history");
export const getMetrics = () => api.get("/api/metrics");

export default api;
