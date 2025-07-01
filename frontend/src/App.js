// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from "react-router-dom";

import UserLogin from "./components/UserLogin";
import UserRegister from "./components/UserRegister";
import AdminLogin from "./components/AdminLogin";
import AdminDashboard from "./components/AdminDashboard";

export default function App() {
  const [adminLoggedIn, setAdminLoggedIn] = useState(false);

  return (
    <Router>
      <nav>
        <Link to="/">User Login</Link> |{" "}
        <Link to="/register">User Register</Link> |{" "}
        <Link to="/admin/login">Admin Login</Link> |{" "}
        <Link to="/admin">Admin Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<UserLogin />} />

        <Route path="/register" element={<UserRegister />} />
        
        <Route
          path="/admin/login"
          element={<AdminLogin onLogin={setAdminLoggedIn} />}
        />

        <Route
          path="/admin"
          element={
            adminLoggedIn ? (
              <AdminDashboard onLogout={() => setAdminLoggedIn(false)} />
            ) : (
              <Navigate to="/admin/login" />
            )
          }
        />

        <Route path="*" element={<div>Pagina non trovata</div>} />
      </Routes>
    </Router>
  );
}
