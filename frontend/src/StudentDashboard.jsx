
import { useEffect, useState } from "react";
import {
  BookOpen,
  ClipboardList,
  GraduationCap,
  LogOut,
  RefreshCw,
  Sun,
  Moon,
  LayoutDashboard,
  ChevronRight,
  CalendarDays,
  CheckCircle2,
} from "lucide-react";
import { applyTheme } from "./theme";
import "./dashboard.css";

const API_URL = "http://127.0.0.1:8000/api/dashboard/student/";

export default function StudentDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [darkMode, setDarkMode] = useState(
    () => localStorage.getItem("trax-theme") !== "light"
  );

  const studentId = new URLSearchParams(
    window.location.search
  ).get("student_id");

  useEffect(() => {
    applyTheme(darkMode ? "dark" : "light");
  }, [darkMode]);

  async function loadDashboard() {
    if (!studentId) {
      setError("Student ID is missing. Please log in again.");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}?student_id=${encodeURIComponent(studentId)}`
      );
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Unable to load dashboard.");
      }

      setData(result);
    } catch (err) {
      setError(err.message || "Could not connect to Django.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, [studentId]);

  function logout() {
    window.location.href = "/";
  }

  const student = data?.student;
  const stats = data?.stats;
  const courses = data?.courses ?? [];
  const grades = data?.grades ?? [];

  if (loading && !data) {
    return (
      <div className="trax-loading">
        <div className="trax-loader-logo">
          <GraduationCap size={32} />
        </div>
        <h2>Trax Solutions</h2>
        <p>Preparing your student workspace...</p>
        <div className="trax-loading-bar"><span /></div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="trax-state">
        <div className="trax-state-icon">
          <RefreshCw size={25} />
        </div>
        <h2>Unable to load your dashboard</h2>
        <p>{error}</p>
        <div className="trax-state-actions">
          <button
            className="trax-primary-button"
            onClick={loadDashboard}
          >
            <RefreshCw size={16} /> Try again
          </button>
          <button
            className="trax-secondary-button"
            onClick={logout}
          >
            Back to login
          </button>
        </div>
      </div>
    );
  }

  if (!student) {
    return (
      <div className="trax-state">
        <h2>Student data unavailable</h2>
        <button className="trax-primary-button" onClick={logout}>
          Return to login
        </button>
      </div>
    );
  }

  return (
    <div className={`trax-app ${darkMode ? "theme-dark" : "theme-light"}`}>
      <aside className="trax-sidebar">
        <a className="trax-brand" href="#overview">
          <span className="trax-brand-mark">
            <GraduationCap size={27} />
          </span>
          <span className="trax-brand-copy">
            <strong>Trax<span>Solutions</span></strong>
            <small>LEARN · MANAGE · GROW</small>
          </span>
        </a>

        <div className="trax-workspace-label">WORKSPACE</div>

        <nav className="trax-navigation">
          <a className="trax-nav-item active" href="#overview">
            <LayoutDashboard size={19} />
            <span>Overview</span>
            <ChevronRight className="trax-nav-chevron" size={16} />
          </a>
          <a className="trax-nav-item" href="#courses">
            <BookOpen size={19} />
            <span>My Courses</span>
          </a>
          <a className="trax-nav-item" href="#grades">
            <ClipboardList size={19} />
            <span>My Assessments</span>
          </a>
        </nav>

        <div className="trax-sidebar-bottom">
          <div className="trax-help-card">
            <span className="trax-help-icon">
              <GraduationCap size={18} />
            </span>
            <strong>Keep learning</strong>
            <p>Every step forward builds your future.</p>
          </div>

          <div className="trax-sidebar-user">
            <div className="trax-avatar">
              {student.name?.charAt(0).toUpperCase() || "S"}
            </div>
            <div className="trax-user-details">
              <strong>{student.name}</strong>
              <small>Student</small>
            </div>
            <button
              className="trax-logout-icon"
              onClick={logout}
              aria-label="Log out"
              title="Log out"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </aside>

      <main className="trax-main">
        <header className="trax-topbar">
          <div className="trax-breadcrumb">
            <span>Workspace</span>
            <ChevronRight size={15} />
            <strong>Student dashboard</strong>
          </div>

          <div className="trax-topbar-actions">
            <button
              className="trax-icon-button trax-theme-toggle"
              onClick={() => setDarkMode(value => !value)}
              aria-label={
                darkMode ? "Switch to light theme" : "Switch to dark theme"
              }
              title={
                darkMode ? "Switch to light theme" : "Switch to dark theme"
              }
            >
              {darkMode ? <Sun size={19} /> : <Moon size={19} />}
            </button>

            <button
              className="trax-icon-button"
              onClick={loadDashboard}
              disabled={loading}
              aria-label="Refresh dashboard"
              title="Refresh dashboard"
            >
              <RefreshCw
                size={18}
                className={loading ? "trax-spin" : ""}
              />
            </button>

            <div className="trax-topbar-profile">
              <div className="trax-avatar small-avatar">
                {student.name?.charAt(0).toUpperCase() || "S"}
              </div>
              <div>
                <strong>{student.name}</strong>
                <small>Student</small>
              </div>
            </div>
          </div>
        </header>

        <div className="trax-content">
          <section className="trax-welcome" id="overview">
            <div className="trax-welcome-content">
              <div className="trax-eyebrow">
                <span className="trax-eyebrow-dot" />
                STUDENT PORTAL
              </div>
              <h1>
                Welcome back, <span>{student.name.split(" ")[0]}!</span>
              </h1>
              <p>
                Your courses, assessments and learning progress — all in one place.
              </p>
              <div className="trax-welcome-meta">
                <span><CalendarDays size={15} /> Your learning overview</span>
                <span><CheckCircle2 size={15} /> Workspace ready</span>
              </div>
            </div>

            <div className="trax-welcome-art" aria-hidden="true">
              <div className="trax-orbit orbit-one" />
              <div className="trax-orbit orbit-two" />
              <div className="trax-art-glow" />
              <div className="trax-art-card art-card-one">
                <BookOpen size={25} />
              </div>
              <div className="trax-art-card art-card-two">
                <ClipboardList size={23} />
              </div>
              <div className="trax-art-center">
                <GraduationCap size={52} />
              </div>
              <div className="trax-art-dot" />
            </div>
          </section>

          <section className="trax-section-heading">
            <div>
              <h2>Learning overview</h2>
              <p>Here's how you're progressing with your studies.</p>
            </div>
            <button
              className="trax-secondary-button"
              onClick={loadDashboard}
              disabled={loading}
            >
              <RefreshCw
                size={15}
                className={loading ? "trax-spin" : ""}
              />
              Refresh data
            </button>
          </section>

          {error && (
            <div className="trax-inline-error">
              {error}
              <button onClick={loadDashboard}>Retry</button>
            </div>
          )}

          <section className="trax-stats-grid">
            <article className="trax-stat-card">
              <div className="trax-stat-top">
                <span className="trax-stat-icon cyan">
                  <BookOpen size={22} />
                </span>
                <span className="trax-stat-tag">Courses</span>
              </div>
              <p>Enrolled courses</p>
              <div className="trax-stat-value">
                {stats?.course_count ?? courses.length}
              </div>
              <div className="trax-stat-foot">
                <span className="trax-stat-foot-icon cyan-text">
                  <BookOpen size={14} />
                </span>
                <span>Courses you're learning</span>
              </div>
              <div className="trax-stat-accent accent-cyan" />
            </article>

            <article className="trax-stat-card">
              <div className="trax-stat-top">
                <span className="trax-stat-icon violet">
                  <ClipboardList size={22} />
                </span>
                <span className="trax-stat-tag">Assessments</span>
              </div>
              <p>Assessments graded</p>
              <div className="trax-stat-value">
                {stats?.assessment_count ?? grades.length}
              </div>
              <div className="trax-stat-foot">
                <span className="trax-stat-foot-icon violet-text">
                  <ClipboardList size={14} />
                </span>
                <span>Results available</span>
              </div>
              <div className="trax-stat-accent accent-violet" />
            </article>

            <article className="trax-stat-card">
              <div className="trax-stat-top">
                <span className="trax-stat-icon green">
                  <GraduationCap size={22} />
                </span>
                <span className="trax-stat-tag">Performance</span>
              </div>
              <p>Average score</p>
              <div className="trax-stat-value">
                {stats?.average_score_percentage ?? 0}%
              </div>
              <div className="trax-stat-foot">
                <span className="trax-stat-foot-icon green-text">
                  <CheckCircle2 size={14} />
                </span>
                <span>Your overall performance</span>
              </div>
              <div className="trax-stat-accent accent-green" />
            </article>
          </section>

          <section
            className="trax-section-heading trax-list-heading"
            id="courses"
          >
            <div>
              <h2>My enrolled courses</h2>
              <p>Review the courses you're currently enrolled in.</p>
            </div>
            <span className="trax-count-pill">
              {courses.length} courses
            </span>
          </section>

          <section className="trax-panel">
            <div className="trax-panel-heading">
              <div className="trax-panel-title">
                <span className="trax-panel-title-icon">
                  <BookOpen size={18} />
                </span>
                <div>
                  <h3>Course directory</h3>
                  <p>Your current learning schedule</p>
                </div>
              </div>
              <span className="trax-count-pill">
                {courses.length} courses
              </span>
            </div>

            {courses.length === 0 ? (
              <div className="trax-empty">
                <span className="trax-empty-icon">
                  <BookOpen size={25} />
                </span>
                <h3>No courses enrolled yet</h3>
                <p>Your enrolled courses will appear here when available.</p>
              </div>
            ) : (
              <div className="trax-table-scroll">
                <table className="trax-table">
                  <thead>
                    <tr>
                      <th>COURSE</th>
                      <th>TRAINER</th>
                      <th>START DATE</th>
                      <th>END DATE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {courses.map(course => (
                      <tr key={course.course_id}>
                        <td>
                          <div className="trax-course-cell">
                            <span className="trax-course-icon">
                              <BookOpen size={19} />
                            </span>
                            <div className="trax-course-info">
                              <strong>{course.course_name}</strong>
                              <small>
                                {course.description || "No course description available"}
                              </small>
                            </div>
                          </div>
                        </td>
                        <td>{course.trainer_name || "Not assigned"}</td>
                        <td>
                          <span className="trax-date">
                            {course.start_date || "—"}
                          </span>
                        </td>
                        <td>
                          <span className="trax-date">
                            {course.end_date || "—"}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          <section
            className="trax-section-heading trax-assessment-heading"
            id="grades"
          >
            <div>
              <h2>My assessments and grades</h2>
              <p>Review your assessment scores and results.</p>
            </div>
            <span className="trax-count-pill">
              {grades.length} results
            </span>
          </section>

          <section className="trax-panel">
            {grades.length === 0 ? (
              <div className="trax-empty">
                <span className="trax-empty-icon">
                  <ClipboardList size={25} />
                </span>
                <h3>No grades available yet</h3>
                <p>Your assessment results will appear here once recorded.</p>
              </div>
            ) : (
              <div className="trax-table-scroll">
                <table className="trax-table">
                  <thead>
                    <tr>
                      <th>ASSESSMENT</th>
                      <th>COURSE</th>
                      <th>TYPE</th>
                      <th>SCORE</th>
                      <th>PERCENTAGE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {grades.map(grade => (
                      <tr key={grade.grade_id}>
                        <td>
                          <div className="trax-assessment-cell">
                            <span className="trax-assessment-icon">
                              <ClipboardList size={18} />
                            </span>
                            <div className="trax-course-info">
                              <strong>{grade.assessment_name}</strong>
                            </div>
                          </div>
                        </td>
                        <td>{grade.course_name}</td>
                        <td>
                          <span className="trax-type-pill">
                            {grade.assessment_type || "General"}
                          </span>
                        </td>
                        <td>
                          <strong>
                            {grade.score} / {grade.max_score}
                          </strong>
                        </td>
                        <td>
                          <span className="trax-number-pill">
                            {grade.percentage ?? "—"}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          <footer className="trax-footer">
            <span>© {new Date().getFullYear()} Trax Solutions</span>
            <span>LEARN <i /> MANAGE <i /> GROW</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
