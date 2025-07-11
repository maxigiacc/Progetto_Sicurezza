// src/App.js
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import UserLogin from "./components/UserLogin";
import UserRegister from "./components/UserRegister";
import UserRequestInvite from "./components/UserRequestInvite";


export default function App() {

  return (
    <Router>
      <nav>
        <Link to="/">Invite</Link> |{" "}
        <Link to="/register">User Register</Link>  |{" "}
        <Link to="/login">User Login</Link>
      </nav>

      <Routes>
        <Route path="/" element={<UserRequestInvite />} />

        <Route path="/login" element={<UserLogin />} />

        <Route path="/register" element={<UserRegister />} />

        <Route path="*" element={<div>Pagina non trovata</div>} />
      </Routes>
    </Router>
  );
}
