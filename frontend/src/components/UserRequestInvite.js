import React, { useState } from "react";

export default function UserRequestInvite() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const requestInvite = async () => {
    setMessage("Invio richiesta...");
    try {
      const res = await fetch("http://localhost:8000/request-invite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      

      const data = await res.json();
      if (res.ok) {
        setMessage("Codice inviato via email!");
      } else {
        setMessage("Errore: " + (data.detail || "Errore sconosciuto"));
      }
    } catch {
      setMessage("Errore di connessione");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "auto", fontFamily: "Arial" }}>
      <h2>Richiedi Codice di Invito</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <button onClick={requestInvite} style={{ width: "100%" }}>
        Richiedi Codice
      </button>
      <p style={{ marginTop: 20, color: "blue" }}>{message}</p>
    </div>
  );
}
