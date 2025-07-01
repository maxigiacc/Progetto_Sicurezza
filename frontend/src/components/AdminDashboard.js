import React from "react";

export default function AdminDashboard({ onLogout }) {
  const [formData, setFormData] = React.useState({
    email_from: "",
    smtp_username: "",
    smtp_password: "",
    smtp_server: "",
    smtp_port: 587,
    smtp_starttls: true,
    smtp_ssl_tls: false,
  });

  const [message, setMessage] = React.useState("");
  const [inviteCode, setInviteCode] = React.useState("");
  const [regEmail, setRegEmail] = React.useState("");
  const [regCode, setRegCode] = React.useState("");
  const [regMessage, setRegMessage] = React.useState("");

  const API_KEY = "SUPERSEGRETO";

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/admin/email_account", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: API_KEY,
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json();
        setMessage("Errore: " + (errorData.detail || "Errore sconosciuto"));
        return;
      }

      const data = await res.json();
      setMessage("Account email aggiunto con successo, ID: " + data.id);
    } catch (error) {
      setMessage("Errore di connessione");
    }
  };

  // Funzione per generare codice invito
  const generateInviteCode = async () => {
    try {
      const res = await fetch("http://localhost:8000/admin/invite", {
        method: "POST",
        headers: {
          Authorization: API_KEY,
        },
      });
      if (!res.ok) {
        const error = await res.json();
        setInviteCode("Errore: " + (error.detail || "Errore generazione codice"));
        return;
      }
      const data = await res.json();
      setInviteCode(data.invite_code);
    } catch (err) {
      setInviteCode("Errore di connessione");
    }
  };

  // Funzione per registrare utente con codice invito
  const registerUser = async () => {
    if (!regEmail || !regCode) {
      setRegMessage("Inserisci email e codice invito");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: regEmail, code: regCode }),
      });
      if (!res.ok) {
        const error = await res.json();
        setRegMessage("Errore: " + (error.detail || "Errore registrazione"));
        return;
      }
      const data = await res.json();
      setRegMessage(data.msg);
    } catch (err) {
      setRegMessage("Errore di connessione");
    }
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <button onClick={onLogout}>Logout Admin</button>

      {/* Form per account email */}
      <form onSubmit={handleSubmit}>
        <input
          name="email_from"
          type="email"
          placeholder="Email from"
          value={formData.email_from}
          onChange={handleChange}
          required
        />
        <input
          name="smtp_username"
          placeholder="SMTP username"
          value={formData.smtp_username}
          onChange={handleChange}
          required
        />
        <input
          name="smtp_password"
          type="password"
          placeholder="SMTP password"
          value={formData.smtp_password}
          onChange={handleChange}
          required
        />
        <input
          name="smtp_server"
          placeholder="SMTP server"
          value={formData.smtp_server}
          onChange={handleChange}
          required
        />
        <input
          name="smtp_port"
          type="number"
          placeholder="SMTP port"
          value={formData.smtp_port}
          onChange={handleChange}
          required
        />
        <label>
          <input
            name="smtp_starttls"
            type="checkbox"
            checked={formData.smtp_starttls}
            onChange={handleChange}
          />
          SMTP STARTTLS
        </label>
        <label>
          <input
            name="smtp_ssl_tls"
            type="checkbox"
            checked={formData.smtp_ssl_tls}
            onChange={handleChange}
          />
          SMTP SSL/TLS
        </label>
        <button type="submit">Aggiungi Email Account</button>
      </form>
      <p>{message}</p>

      {/* Sezione codice invito */}
      <hr />
      <h3>Genera Codice Invito</h3>
      <button onClick={generateInviteCode}>Genera Codice</button>
      {inviteCode && <p>Codice Invito: {inviteCode}</p>}

      {/* Sezione registrazione utente */}
      <hr />
      <h3>Registra Utente</h3>
      <input
        type="email"
        placeholder="Email utente"
        value={regEmail}
        onChange={(e) => setRegEmail(e.target.value)}
      />
      <input
        type="text"
        placeholder="Codice invito"
        value={regCode}
        onChange={(e) => setRegCode(e.target.value)}
      />
      <button onClick={registerUser}>Registra</button>
      <p>{regMessage}</p>
    </div>
  );
}
