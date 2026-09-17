export interface ApiErrorPayload {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}