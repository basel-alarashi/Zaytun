/**
 * Typed representation of Zaytun's canonical API error contract
 * (see 10_API_Specification.md §12). Thrown by apiClient for every
 * non-2xx response, so callers can branch on `.code` instead of
 * inspecting raw HTTP status codes or unparsed bodies.
 */
import type { ApiErrorPayload } from '../types/errors';

export class ApiError extends Error {
  readonly code: string;
  readonly status: number;
  readonly details: Record<string, unknown>;

  constructor(status: number, payload: ApiErrorPayload) {
    super(payload.message);
    this.name = "ApiError";
    this.code = payload.code;
    this.status = status;
    this.details = payload.details ?? {};
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env and fill it in."
  );
}

const UNSAFE_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"]);

function getCookie(name: string): string | null {
  const match = document.cookie.match(
    new RegExp(`(?:^|; )${name}=([^;]*)`)
  );
  return match ? decodeURIComponent(match[1]) : null;
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
}

function isErrorPayload(value: unknown): value is ApiErrorPayload {
  return (
    typeof value === "object" &&
    value !== null &&
    "code" in value &&
    "message" in value
  );
}

/**
 * Thin fetch wrapper. Components should never call fetch() directly —
 * going through here keeps base-URL resolution, session-cookie credentials
 * and CSRF header attachment (ADR-007), and error shaping in one place
 * instead of duplicated per call site.
 */
async function request<TResponse>(
  path: string,
  { body, headers, ...options }: RequestOptions = {}
): Promise<TResponse> {
  const method = (options.method ?? "GET").toUpperCase();
  const csrfToken = UNSAFE_METHODS.has(method) ? getCookie("csrftoken") : null;

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    method,
    credentials: "include",
    headers: {
      Accept: "application/json",
      ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  // 204 No Content has no body to parse; anything else may or may not be JSON.
  const data =
    response.status === 204 ? null : await response.json().catch(() => null);

  if (!response.ok) {
    if (isErrorPayload(data)) {
      throw new ApiError(response.status, data);
    }
    throw new ApiError(response.status, {
      code: "UNKNOWN_ERROR",
      message: `Request failed with status ${response.status}.`,
    });
  }

  return data as TResponse;
}

export const apiClient = {
  get: <TResponse>(path: string, options?: RequestOptions) =>
    request<TResponse>(path, { ...options, method: "GET" }),
  post: <TResponse>(path: string, body?: unknown, options?: RequestOptions) =>
    request<TResponse>(path, { ...options, method: "POST", body }),
  patch: <TResponse>(path: string, body?: unknown, options?: RequestOptions) =>
    request<TResponse>(path, { ...options, method: "PATCH", body }),
  delete: <TResponse>(path: string, options?: RequestOptions) =>
    request<TResponse>(path, { ...options, method: "DELETE" }),
};