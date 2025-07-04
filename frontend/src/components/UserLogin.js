// src/components/UserLogin.js
import React, { useState } from "react";

export default function UserLogin() {
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [jwt, setJwt] = useState(localStorage.getItem("jwt") || "");
  const [message, setMessage] = useState("");

  async function requestMagicLink() {
    setMessage("Invio richiesta...");
    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        setMessage("Link inviato! Controlla la tua email.");
      } else {
        const data = await res.json();
        setMessage("Errore: " + (data.detail || "Errore sconosciuto"));
      }
    } catch (e) {
      setMessage("Errore di connessione");
    }
  }

  async function verifyMagicToken() {
    setMessage("Verifico token...");
    try {
      const res = await fetch(`http://localhost:8000/verify?token=${token}`);
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("jwt", data.access_token);
        setJwt(data.access_token);
        setMessage("Login effettuato con successo!");
      } else {
        setMessage("Errore: " + (data.detail || "Token non valido"));
      }
    } catch (e) {
      setMessage("Errore di connessione");
    }
  }

  async function callProtectedEndpoint() {
    if (!jwt) {
      setMessage("Devi prima effettuare il login");
      return;
    }
    setMessage("Chiamata endpoint protetto...");
    try {
      const res = await fetch("http://localhost:8000/protected", {
        headers: { Authorization: "Bearer " + jwt },
      });
      const data = await res.json();
      if (res.ok) {
        setMessage("Risposta: " + data.msg);
      } else {
        setMessage("Errore: " + (data.detail || "Errore sconosciuto"));
      }
    } catch (e) {
      setMessage("Errore di connessione");
    }
  }

  function logout() {
    localStorage.removeItem("jwt");
    setJwt("");
    setMessage("Logout effettuato");
  }

  return (
    <div style={{ maxWidth: 400, margin: "auto", fontFamily: "Arial" }}>
      <h1>Login Magic Link - Ethereal</h1>
      <label>
        Email Ethereal:<br />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="esempio@ethereal.email"
          style={{ width: "100%", marginBottom: 10 }}
        />
      </label>
      <button onClick={requestMagicLink} style={{ width: "100%" }}>
        Richiedi Magic Link
      </button>

      <hr />

      <label>
        Inserisci Token Magic Link:<br />
        <input
          type="text"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Token ricevuto via email"
          style={{ width: "100%", marginBottom: 10 }}
        />
      </label>
      <button onClick={verifyMagicToken} style={{ width: "100%" }}>
        Verifica Token
      </button>

      <hr />

      <button onClick={callProtectedEndpoint} style={{ width: "100%" }}>
        Accedi a Endpoint Protetto
      </button>

      <button onClick={logout} style={{ width: "100%", marginTop: 10 }}>
        Logout
      </button>

      <p style={{ marginTop: 20, color: "blue" }}>{message}</p>
    </div>
  );
}
