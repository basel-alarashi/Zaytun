import { apiClient } from "../../lib/apiClient";
import type { User } from "./types";

export interface RegisterInput {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  role?: "CONSUMER" | "FARMER";
}

export interface LoginInput {
  email: string;
  password: string;
}

export const authApi = {
  ensureCsrfCookie: () => apiClient.get<{ detail: string }>("/auth/csrf/"),
  me: () => apiClient.get<User>("/auth/me/"),
  register: (data: RegisterInput) => apiClient.post<User>("/auth/register/", data),
  login: (data: LoginInput) => apiClient.post<User>("/auth/login/", data),
  logout: () => apiClient.post<void>("/auth/logout/"),
};