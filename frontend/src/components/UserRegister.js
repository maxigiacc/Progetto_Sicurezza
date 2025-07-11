// src/components/UserRegister.js
import React, { useState } from "react";

export default function UserRegister() {
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");

  async function handleRegister() {
    setMessage("Registrazione in corso...");
    try {
      const res = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, code }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage(data.msg);
      } else {
        setMessage("Errore: " + (data.detail || "Errore sconosciuto"));
      }
    } catch (e) {
      setMessage("Errore di connessione");
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "auto", fontFamily: "Arial" }}>
      <h1>Registrazione Utente</h1>

      <label>
        Email:<br />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="tuo@email.com"
          style={{ width: "100%", marginBottom: 10 }}
        />
      </label>

      <label>
        Codice Invito:<br />
        <input
          type="password"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Inserisci codice invito"
          style={{ width: "100%", marginBottom: 10 }}
        />
      </label>

      <button onClick={handleRegister} style={{ width: "100%" }}>
        Registrati
      </button>

      <p style={{ marginTop: 20, color: message.startsWith("Errore") ? "red" : "green" }}>
        {message}
      </p>
    </div>
  );
}
