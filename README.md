# 🛡️ Progetto Sicurezza

Un'applicazione che implementa un sistema sicuro di accesso passwordless, con inviti via email e protezione tramite rate limiting e API Key.

## 🚀 Funzionalità principali

- Richiesta invito via email
- Registrazione con codice invito
- Login passwordless
- Verifica token JWT e generazione access token
- Accesso a risorse protette tramite JWT
- API protette da API Key e rate limiting

## 🧠 Tecnologie usate

### Backend
- FastAPI
- JWT (`python-jose`)
- Rate limiting (`slowapi`)
- Invio email personalizzato
- Protezione con API Key

### Frontend
- React
- React Router
- Componenti: `UserLogin`, `UserRegister`, `UserRequestInvite`

## ⚙️ Installazione

### Backend

1. Clona la repo:

   ```
   git clone https://github.com/maxigiacc/Progetto_Sicurezza.git
   cd Progetto_Sicurezza/app
   ```

2. Crea e attiva un ambiente virtuale:

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Installa le dipendenze:

   ```
   pip install -r ../requirements.txt
   ```

4. Avvia il backend, nella root del progetto:

   ```
   python -m uvicorn app.main:app --reload
   ```

### Frontend

1. Apri un nuovo terminale e vai nella cartella:

   ```
   cd ../frontend
   ```

2. Installa le dipendenze:

   ```
   npm install
   ```

3. Avvia l'app:

   ```
   npm start
   ```

## 📬 API principali

| Metodo | Endpoint            | Descrizione                              |
|--------|---------------------|------------------------------------------|
| POST   | /request-invite     | Invia un codice invito via email         |
| POST   | /register           | Registra l’utente con codice invito      |
| POST   | /login              | Invia magic link per autenticazione      |
| GET    | /verify?token=...   | Verifica token e genera access token JWT |
| GET    | /protected          | Accesso risorsa protetta con JWT         |

> Tutte le richieste devono includere l’header:  
> `Authorization: SUPERSEGRETO`

## 🧪 Flusso utente

1. L’utente richiede un invito → riceve un codice via email
2. Si registra con l’indirizzo email e il codice
3. Inserisce la propria email per ricevere un magic link
4. Clicca il link → verifica il token → riceve un access token
5. Accede a contenuti protetti con il JWT

## 🔐 Sicurezza

- Rate limit per il login: 5 richieste al minuto
- Accesso solo con codice invito
- Login senza password via magic link (token temporaneo)
- JWT per accesso autenticato
- Protezione tramite API Key in tutte le chiamate

## 📦 Dipendenze principali

```
fastapi
uvicorn
sqlalchemy
slowapi
python-jose
pydantic
email-validator
```


## 📁 Configurazione `.env`

Per il corretto funzionamento dell'invio email, è necessario creare un file `.env` nella cartella `app/` con il seguente contenuto:

```
SECRET_KEY="una_chiave_super_segreta"
EMAIL_FROM="la_tua_email@gmail.com"
MAIL_USERNAME="la_tua_email@gmail.com"
MAIL_PASSWORD="password_dell_app"
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_FROM_NAME="Progetto Sicurezza"
MAIL_STARTTLS=True
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```

### 📧 Come ottenere `MAIL_PASSWORD` per Gmail

Per usare un account Gmail in sicurezza, non devi usare la tua password normale, ma una **password per le app**:

1. Vai su [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Accedi con il tuo account Google
3. Seleziona l'app (es. "Mail") e il dispositivo (es. "Altro – Progetto Sicurezza")
4. Google genererà una password a 16 caratteri
5. Usa quella password nel campo `MAIL_PASSWORD` del tuo `.env`

> ℹ️ Le password per le app richiedono che l’autenticazione a due fattori sia attiva sul tuo account Google.

> ⚠️ Non condividere questo file pubblicamente. Assicurati di aggiungerlo a `.gitignore`.

### 🧪 Alternativa: usare un account **Ethereal**

Puoi usare un account fittizio con [Ethereal Email](https://ethereal.email/) solo per test:

1. Vai su [https://ethereal.email/create](https://ethereal.email/create)
2. Crea un account temporaneo (ti darà username, password, host, port)
3. Inserisci questi dati nel file `.env`:

```
EMAIL_FROM="utente@ethereal.email"
MAIL_USERNAME="utente@ethereal.email"
MAIL_PASSWORD="la_password"
MAIL_SERVER="smtp.ethereal.email"
MAIL_PORT=587
MAIL_FROM_NAME="Progetto Sicurezza"
MAIL_STARTTLS=True
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```
> ⚠️ Ethereal serve solo per test: le email non vengono effettivamente consegnate all’utente, ma visualizzate nella mailbox relativa all'utente ethereal creato.


## 📄 Licenza

Distribuito sotto licenza MIT. Vedi il file `LICENSE`.

## 👨‍💻 Autore

Progetto sviluppato da [@maxigiacc](https://github.com/maxigiacc)

