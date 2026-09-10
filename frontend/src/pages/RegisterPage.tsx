import { useState, type SubmitEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { ApiError } from "../lib/apiClient";

type FieldErrors = Record<string, string[]>;

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [role, setRole] = useState<"CONSUMER" | "FARMER">("CONSUMER");
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormError(null);
    setFieldErrors({});
    setSubmitting(true);

    try {
      await register({ email, password, first_name: firstName, last_name: lastName, role });
      navigate("/", { replace: true });
    } catch (error) {
      if (error instanceof ApiError && error.code === "VALIDATION_ERROR") {
        setFieldErrors(error.details as FieldErrors);
      } else {
        setFormError(
          error instanceof ApiError ? error.message : "Something went wrong. Please try again."
        );
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main>
      <h1>Create an account</h1>
      <form onSubmit={handleSubmit} noValidate>
        <div>
          <label htmlFor="register-email">Email</label>
          <input
            id="register-email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          {fieldErrors.email && <p role="alert">{fieldErrors.email.join(" ")}</p>}
        </div>
        <div>
          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            type="password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          {fieldErrors.password && <p role="alert">{fieldErrors.password.join(" ")}</p>}
        </div>
        <div>
          <label htmlFor="register-first-name">First name</label>
          <input
            id="register-first-name"
            type="text"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="register-last-name">Last name</label>
          <input
            id="register-last-name"
            type="text"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="register-role">I am a</label>
          <select
            id="register-role"
            value={role}
            onChange={(event) => setRole(event.target.value as "CONSUMER" | "FARMER")}
          >
            <option value="CONSUMER">Consumer</option>
            <option value="FARMER">Farmer</option>
          </select>
        </div>
        {formError && <p role="alert">{formError}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? "Creating account…" : "Create account"}
        </button>
      </form>
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </main>
  );
}