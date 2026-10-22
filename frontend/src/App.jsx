import Login from "./pages/Login";
import StudentDashboard from "./StudentDashboard";
import InstructorDashboard from "./InstructorDashboard";

function App() {
  const path = window.location.pathname;

  console.log("Current path:", path);

  if (path === "/student-dashboard") {
    return <StudentDashboard />;
  }

  if (path === "/instructor-dashboard") {
    return <InstructorDashboard />;
  }

  return <Login />;
}

export default App;
