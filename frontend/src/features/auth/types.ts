import { type LoginInput, type RegisterInput } from "./authApi";

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: "CONSUMER" | "FARMER" | "ADMIN";
  date_joined: string;
}

export type AuthStatus = "loading" | "authenticated" | "anonymous";

export interface AuthContextValue {
  user: User | null;
  status: AuthStatus;
  // eslint-disable-next-line no-unused-vars
  login(_data: LoginInput): Promise<void>;
  // eslint-disable-next-line no-unused-vars
  register(_data: RegisterInput): Promise<void>;
  logout: () => Promise<void>;
}