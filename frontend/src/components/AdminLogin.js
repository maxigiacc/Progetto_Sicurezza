// src/components/AdminLogin.js
import React, { useState } from "react";

export default function AdminLogin({ onLogin }) {
  const [apiKey, setApiKey] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = () => {
    if (apiKey === "supersegretoapikey123") {
      onLogin(true);
    } else {
      setMessage("API Key non valida");
    }
  };

  return (
    <div>
      <h2>Login Admin</h2>
      <input
        type="password"
        placeholder="API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      <p style={{ color: "red" }}>{message}</p>
    </div>
  );
}
