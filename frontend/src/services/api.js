import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 12000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function askStudyBot(question) {
  const response = await api.post("/ask", { question });
  return response.data;
}

export async function checkBackendHealth() {
  const response = await api.get("/health");
  return response.data;
}

export default api;
