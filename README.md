# 📧 EMAIL-AI-AGENT

> An autonomous AI agent that monitors your Gmail inbox, understands incoming emails, and sends intelligent context-aware replies — fully automated using **Google Gemini AI**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange?style=flat-square)
![Gmail](https://img.shields.io/badge/Gmail-IMAP%2FSMTP-red?style=flat-square)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-ff4b4b?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Type](https://img.shields.io/badge/Type-AI_Agent-purple?style=flat-square)

---

## 🤖 What is an AI Agent?

This project is a true **AI Agent** — not just a script or tool:

| Step | What it does |
|------|-------------|
| 👁️ **Perceive** | Reads unread emails from your Gmail inbox via IMAP |
| 🧠 **Reason** | Sends email content to Google Gemini to understand context and generate a reply |
| ⚡ **Act** | Automatically sends the AI-generated reply via SMTP |
| 🔁 **Loop** | Repeats every 30 seconds — fully autonomous, zero human input |

---

## ✨ Features

- 📥 Monitors Gmail inbox for unread emails automatically
- 🤖 Generates professional, context-aware replies using Gemini 1.5 Flash
- 📤 Sends replies automatically via Gmail SMTP
- 🖥️ **Live Streamlit Dashboard** — monitor the agent in real time via browser
- 🔐 Secure credential management via `.env` file — no hardcoded secrets
- 🛡️ Per-email error handling — one failure won't crash the agent
- ♾️ Runs continuously in a loop every 30 seconds
- ✅ Config validation at startup with clear error messages

---

## 🖥️ Live Dashboard

Run the agent with a visual dashboard in your browser:

```bash
streamlit run dashboard.py
```

Dashboard includes:
- 🟢 Live status indicator (RUNNING / STOPPED)
- 📊 Real-time metrics: Emails Processed, Replies Sent, Errors, Uptime
- ▶️ Start / ⏹️ Stop agent controls
- 📋 Color-coded activity log
- ✅ .env config status checker
- 📧 Recent emails processed list

---

## 🗂️ Project Structure

```
EMAIL-AI-AGENT/
│
├── dashboard.py       # Streamlit web dashboard
├── main.py            # CLI entry point — runs the agent loop
├── ai_reply.py        # Gemini AI reply generation
├── email_utils.py     # IMAP email fetching + SMTP sending
├── config.py          # Loads and validates environment variables
├── .streamlit/
│   └── config.toml    # Dashboard theme config
├── .env.example       # Credentials template (safe to commit)
├── .env               # Your actual credentials ⚠️ DO NOT COMMIT
├── .gitignore         # Prevents .env from being pushed to GitHub
├── Procfile           # Railway deployment config
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## ⚙️ How It Works

```
Gmail Inbox
     │
     ▼
IMAP (fetch unread emails)
     │
     ▼
Google Gemini 1.5 Flash
(understands email + generates reply)
     │
     ▼
SMTP (sends reply automatically)
     │
     ▼
Wait 30 seconds → repeat
```

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/engineermuhammadtalha/EMAIL-AI-AGENT
cd EMAIL-AI-AGENT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your credentials

```bash
cp .env.example .env
```

Edit `.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_ADDRESS=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here
```

### 4. Run with Dashboard (recommended)

```bash
streamlit run dashboard.py
```

### 4b. Run in CLI mode

```bash
python main.py
```

---

## 🔑 Getting Your Credentials

### Gemini API Key (Free)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key**
3. Paste into `.env`

### Gmail App Password
1. Go to [Google Account](https://myaccount.google.com)
2. Security → 2-Step Verification → **App Passwords**
3. Select **Mail** → **Other** → Copy the 16-character password into `.env`

---

## ☁️ Deploy on Railway (Live 24/7)

1. Go to [railway.app](https://railway.app)
2. **New Project** → Deploy from GitHub → select `EMAIL-AI-AGENT`
3. Go to **Variables** tab and add:
   ```
   GEMINI_API_KEY=...
   EMAIL_ADDRESS=...
   EMAIL_PASSWORD=...
   ```
4. Railway will detect the `Procfile` and serve the dashboard live ✅

---

## 🔐 Security Best Practices

- ✅ All credentials stored in `.env` — never in source code
- ✅ `.env` is in `.gitignore` — will never be committed to GitHub
- ✅ Use `.env.example` as a safe template to share
- ⚠️ Never paste your real API key into any `.py` file
- ⚠️ If you accidentally commit secrets, revoke them immediately at [console.cloud.google.com](https://console.cloud.google.com)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Model | Google Gemini 1.5 Flash |
| Dashboard | Streamlit |
| Email Receiving | Python `imaplib` (IMAP over SSL) |
| Email Sending | Python `smtplib` (SMTP over SSL port 465) |
| Config Management | `python-dotenv` |
| Deployment | Railway |
| Language | Python 3.9+ |

---

## 📦 Requirements

```
google-generativeai
python-dotenv
streamlit
imaplib2
```

---

## ⚠️ Disclaimer

This agent replies **automatically to all unread emails**. Test with a **dedicated Gmail account** before using on your primary inbox.

---

## 📄 License

MIT License

---

## 👤 Author

**Muhammad Talha** — AI Engineer  
🔗 [GitHub](https://github.com/engineermuhammadtalha)

---

> *"A true AI Agent — it perceives, reasons, and acts. Fully autonomous."*
