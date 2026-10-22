
import { useState } from "react";
import {
  Sun,
  Moon,
  GraduationCap,
  ChartNoAxesColumnIncreasing,
  UsersRound,
  UserRound,
  Eye,
  EyeOff,
  ShieldCheck,
  Cpu,
  Database,
  Code2,
  Cloud,
  ArrowRight,
} from "lucide-react";
import "../index.css";

const API_URL = "http://127.0.0.1:8000/api/login/";
const REACT_URL = "http://localhost:5173";

export default function Login() {
  const [role, setRole] = useState("student");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (loading) return;

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      });

      const data = await response.json();

      console.log("Login response:", data);

      if (!response.ok) {
        setMessage(
          data.message || data.error || "Invalid username or password."
        );
        return;
      }

      const returnedRole = String(data.role || "")
        .trim()
        .toLowerCase();

      if (returnedRole !== role) {
        setMessage(
          `This account is registered as ${data.role}. Please select the correct role.`
        );
        return;
      }

      if (returnedRole === "student") {
        if (
          data.student_id === null ||
          data.student_id === undefined ||
          data.student_id === ""
        ) {
          setMessage("Student ID was not returned by the server.");
          return;
        }

        window.location.assign(
          `${REACT_URL}/student-dashboard?student_id=${encodeURIComponent(
            data.student_id
          )}`
        );

        return;
      }

      if (
        returnedRole === "trainer" ||
        returnedRole === "instructor"
      ) {
        if (
          data.trainer_id === null ||
          data.trainer_id === undefined ||
          data.trainer_id === ""
        ) {
          setMessage("Instructor ID was not returned by the server.");
          return;
        }

        window.location.assign(
          `${REACT_URL}/instructor-dashboard?trainer_id=${encodeURIComponent(
            data.trainer_id
          )}`
        );

        return;
      }

      setMessage("This account does not have a supported dashboard.");
    } catch (error) {
      console.error("Login error:", error);

      setMessage(
        "Cannot connect to Django. Check that your backend server is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={`login-page ${darkMode ? "dark-theme" : ""}`}>
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <div className="dot-pattern dots-left" />
      <div className="dot-pattern dots-right" />

      <header className="topbar">
        <a className="brand" href="/" aria-label="Trax Solutions home">
          <img
            className="brand-logo"
            src="/images/t-logo.png"
            alt="Trax Solutions logo"
          />

          <span className="brand-copy">
            <strong>
              Trax <span>Solutions</span>
            </strong>
            <small>LEARN · MANAGE · GROW</small>
          </span>
        </a>

        <button
          type="button"
          className={`theme-toggle ${darkMode ? "is-dark" : ""}`}
          onClick={() => setDarkMode((previous) => !previous)}
          aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
        >
          <span className="theme-thumb" />
          <Sun size={18} />
          <Moon size={18} />
        </button>
      </header>

      <section className="login-layout">
        <section className="hero-section">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            ACADEMIC MANAGEMENT PORTAL
          </div>

          <h1>
            Build Your
            <br />
            Future with <span className="gradient-text">Trax Solutions</span>
          </h1>

          <p className="hero-description">
            A smarter platform for courses, assessments, student records,
            and academic progress.
          </p>

          <div className="feature-list">
            <article className="feature-item">
              <div className="feature-icon course-icon">
                <GraduationCap size={25} />
              </div>
              <h3>Manage Courses</h3>
              <p>Access and track your courses with ease.</p>
            </article>

            <article className="feature-item">
              <div className="feature-icon progress-icon">
                <ChartNoAxesColumnIncreasing size={25} />
              </div>
              <h3>Track Progress</h3>
              <p>Monitor grades and academic performance.</p>
            </article>

            <article className="feature-item">
              <div className="feature-icon people-icon">
                <UsersRound size={25} />
              </div>
              <h3>Stay Connected</h3>
              <p>For students, instructors and admin.</p>
            </article>
          </div>

          <div className="illustration-wrap">
            <div className="illustration-glow" />
            <img
              src="/images/hero-illustration.png"
              alt="Computer with AI, coding and data science illustrations"
              className="hero-illustration"
            />
          </div>

          <div className="learning-note">
            <span>Your Learning</span>
            <span>Journey, Simplified.</span>
            <div className="learning-underline" />
          </div>

          <div className="technology-tags">
            <span><Cpu size={15} /> AI &amp; ML</span>
            <i />
            <span><Database size={15} /> Data Science</span>
            <i />
            <span><Code2 size={15} /> Web Development</span>
            <i />
            <span><Cloud size={15} /> Cloud Computing</span>
          </div>
        </section>

        <section className="form-column">
          <div className="login-card">
            <div className="card-brand">
              <div className="card-logo-wrap">
                <img src="/images/t-logo.png" alt="" />
              </div>
              <div>
                <h2>Trax Solutions</h2>
                <p>Academic Management Portal</p>
              </div>
            </div>

            <div className="welcome-heading">
              <h2>Welcome Back</h2>
              <p>Sign in to continue to your dashboard</p>
            </div>

            <div className="role-switch" aria-label="Choose account type">
              <button
                type="button"
                className={role === "student" ? "selected" : ""}
                onClick={() => {
                  setRole("student");
                  setMessage("");
                }}
              >
                <GraduationCap size={19} />
                Student
              </button>

              <button
                type="button"
                className={role === "trainer" ? "selected" : ""}
                onClick={() => {
                  setRole("trainer");
                  setMessage("");
                }}
              >
                <UsersRound size={19} />
                Instructor
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <label htmlFor="username">Username</label>
              <div className="input-wrap">
                <UserRound className="input-icon" size={19} />
                <input
                  id="username"
                  type="text"
                  autoComplete="username"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
              </div>

              <label htmlFor="password">Password</label>
              <div className="input-wrap">
                <ShieldCheck className="input-icon" size={19} />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((previous) => !previous)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
                </button>
              </div>

              <div className="form-options">
                <label className="remember-option">
                  <input type="checkbox" />
                  <span>Remember me</span>
                </label>

                <button
                  type="button"
                  className="forgot-link"
                  onClick={() =>
                    setMessage(
                      "Please contact your administrator to reset your password."
                    )
                  }
                >
                  Forgot password?
                </button>
              </div>

              {message && (
                <p
                  className={`form-message ${
                    message.startsWith("Login successful")
                      ? "success"
                      : "error"
                  }`}
                  role="status"
                >
                  {message}
                </p>
              )}

              <button
                type="submit"
                className="sign-in-button"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Sign In"}
                {!loading && <ArrowRight size={20} />}
              </button>
            </form>

            <div className="card-footer">
              <span className="footer-line" />
              <span>OR</span>
              <span className="footer-line" />
            </div>

            <p className="security-note">
              <ShieldCheck size={17} />
              Secure access for students and instructors
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}