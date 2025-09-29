import axios from "axios";
const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost/api"; // nginx routes /api -> api:8000
export const api = axios.create({ baseURL: base });
export function setToken(token: string | null) {
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}
