// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import UserLogin from "./components/UserLogin";
import UserRegister from "./components/UserRegister";
import UserRequestInvite from "./components/UserRequestInvite";


export default function App() {

  return (
    <Router>
      <nav>
        <Link to="/">User Login</Link> |{" "}
        <Link to="/register">User Register</Link> |{" "}
        <Link to="/request-invite">Invite</Link>
      </nav>

      <Routes>
        <Route path="/" element={<UserLogin />} />

        <Route path="/register" element={<UserRegister />} />

        <Route path="/request-invite" element={<UserRequestInvite />} />

        <Route path="*" element={<div>Pagina non trovata</div>} />
      </Routes>
    </Router>
  );
}
