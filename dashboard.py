import streamlit as st
import threading
import time
import queue
import json
from datetime import datetime
from collections import deque

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EMAIL-AI-AGENT",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0d14;
    color: #e2e8f0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1400px; }

/* Header */
.agent-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #1e2535;
    padding-bottom: 1.5rem;
}
.agent-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
}
.agent-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.2rem;
}

/* Status pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.9rem;
    border-radius: 100px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.status-running {
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #22c55e;
}
.status-stopped {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #ef4444;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
.dot-green { background: #22c55e; }
.dot-red { background: #ef4444; animation: none; }
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Metric cards */
.metric-card {
    background: #111827;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1;
}
.metric-accent { color: #6366f1; }

/* Log container */
.log-container {
    background: #0d1117;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    max-height: 340px;
    overflow-y: auto;
}
.log-entry { border-bottom: 1px solid #0d1117; padding: 0.2rem 0; }
.log-time { color: #475569; margin-right: 0.5rem; }
.log-info { color: #38bdf8; }
.log-success { color: #22c55e; }
.log-warn { color: #f59e0b; }
.log-error { color: #ef4444; }

/* Email cards */
.email-card {
    background: #111827;
    border: 1px solid #1e2535;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    border-left: 3px solid #6366f1;
}
.email-sender { font-weight: 600; color: #c7d2fe; font-size: 0.9rem; }
.email-subject { color: #94a3b8; font-size: 0.82rem; margin-top: 0.15rem; }
.email-time { color: #475569; font-size: 0.75rem; font-family: 'Space Mono', monospace; }
.email-replied { 
    float: right; font-size: 0.7rem; padding: 0.15rem 0.5rem;
    background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.25);
    border-radius: 100px; color: #22c55e; font-family: 'Space Mono', monospace;
}

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.15s ease !important;
}

/* Section headings */
.section-heading {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2535;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "agent_running" not in st.session_state:
    st.session_state.agent_running = False
if "emails_processed" not in st.session_state:
    st.session_state.emails_processed = 0
if "replies_sent" not in st.session_state:
    st.session_state.replies_sent = 0
if "errors" not in st.session_state:
    st.session_state.errors = 0
if "logs" not in st.session_state:
    st.session_state.logs = deque(maxlen=100)
if "email_history" not in st.session_state:
    st.session_state.email_history = []
if "agent_thread" not in st.session_state:
    st.session_state.agent_thread = None
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
if "log_queue" not in st.session_state:
    st.session_state.log_queue = queue.Queue()
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ── Agent Logic ───────────────────────────────────────────────────────────────
def add_log(level, message, q):
    ts = datetime.now().strftime("%H:%M:%S")
    q.put({"time": ts, "level": level, "msg": message})

def agent_loop(stop_event, log_queue, state_proxy):
    """The actual agent loop that runs in background thread."""
    try:
        from config import validate_config, EMAIL_ADDRESS, EMAIL_PASSWORD, GEMINI_API_KEY
        from email_utils import fetch_unread_emails, send_reply
        from ai_reply import generate_reply

        add_log("info", "⚙️  Config validated. Connecting to Gmail...", log_queue)
        validate_config()
        add_log("success", f"✅ Connected as {EMAIL_ADDRESS}", log_queue)
        add_log("info", "🔄 Agent loop started — polling every 30s", log_queue)

        while not stop_event.is_set():
            try:
                add_log("info", "📥 Checking inbox for unread emails...", log_queue)
                emails = fetch_unread_emails()

                if not emails:
                    add_log("info", "💤 No new emails. Waiting 30s...", log_queue)
                else:
                    for email_data in emails:
                        if stop_event.is_set():
                            break
                        sender = email_data.get("sender", "unknown")
                        subject = email_data.get("subject", "(no subject)")
                        body = email_data.get("body", "")

                        add_log("info", f"📧 Email from {sender} — {subject}", log_queue)
                        state_proxy["emails_processed"] += 1

                        try:
                            reply = generate_reply(body)
                            send_reply(sender, subject, reply)
                            add_log("success", f"✅ Reply sent to {sender}", log_queue)
                            state_proxy["replies_sent"] += 1
                            state_proxy["email_history"].append({
                                "sender": sender,
                                "subject": subject,
                                "time": datetime.now().strftime("%H:%M:%S"),
                                "replied": True,
                            })
                        except Exception as e:
                            add_log("error", f"❌ Failed to reply to {sender}: {e}", log_queue)
                            state_proxy["errors"] += 1

                stop_event.wait(30)

            except Exception as e:
                add_log("error", f"⚠️  Loop error: {e}", log_queue)
                state_proxy["errors"] += 1
                stop_event.wait(10)

    except Exception as e:
        add_log("error", f"🚨 Agent crashed: {e}", log_queue)

    add_log("warn", "🛑 Agent stopped.", log_queue)


# ── Pull log queue into session state ─────────────────────────────────────────
state_proxy = {
    "emails_processed": st.session_state.emails_processed,
    "replies_sent": st.session_state.replies_sent,
    "errors": st.session_state.errors,
    "email_history": st.session_state.email_history,
}

while not st.session_state.log_queue.empty():
    entry = st.session_state.log_queue.get_nowait()
    st.session_state.logs.append(entry)

# Sync counters back
st.session_state.emails_processed = state_proxy["emails_processed"]
st.session_state.replies_sent = state_proxy["replies_sent"]
st.session_state.errors = state_proxy["errors"]

# ── HEADER ────────────────────────────────────────────────────────────────────
is_running = st.session_state.agent_running
status_class = "status-running" if is_running else "status-stopped"
dot_class = "dot-green" if is_running else "dot-red"
status_text = "RUNNING" if is_running else "STOPPED"

st.markdown(f"""
<div class="agent-header">
    <div>
        <div class="agent-title">✉️ EMAIL-AI-AGENT</div>
        <div class="agent-subtitle">Autonomous email agent powered by Google Gemini 1.5 Flash</div>
    </div>
    <div style="margin-left:auto;">
        <div class="status-pill {status_class}">
            <span class="status-dot {dot_class}"></span>
            {status_text}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ROW ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

uptime = "—"
if st.session_state.start_time and is_running:
    secs = int(time.time() - st.session_state.start_time)
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    uptime = f"{h:02d}:{m:02d}:{s:02d}"

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Emails Processed</div>
        <div class="metric-value metric-accent">{st.session_state.emails_processed}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Replies Sent</div>
        <div class="metric-value" style="color:#22c55e">{st.session_state.replies_sent}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Errors</div>
        <div class="metric-value" style="color:#ef4444">{st.session_state.errors}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Uptime</div>
        <div class="metric-value" style="font-size:1.4rem; color:#94a3b8">{uptime}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CONTROLS + LOG ROW ───────────────────────────────────────────────────────
left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="section-heading">Controls</div>', unsafe_allow_html=True)

    if not is_running:
        if st.button("▶  START AGENT", use_container_width=True, type="primary"):
            st.session_state.stop_event = threading.Event()
            st.session_state.emails_processed = 0
            st.session_state.replies_sent = 0
            st.session_state.errors = 0
            st.session_state.logs = deque(maxlen=100)
            st.session_state.email_history = []
            st.session_state.start_time = time.time()
            t = threading.Thread(
                target=agent_loop,
                args=(st.session_state.stop_event, st.session_state.log_queue, state_proxy),
                daemon=True,
            )
            st.session_state.agent_thread = t
            t.start()
            st.session_state.agent_running = True
            st.rerun()
    else:
        if st.button("⏹  STOP AGENT", use_container_width=True):
            st.session_state.stop_event.set()
            st.session_state.agent_running = False
            st.session_state.start_time = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄  Refresh", use_container_width=True):
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Config status check
    st.markdown('<div class="section-heading">Config Status</div>', unsafe_allow_html=True)
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        checks = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "EMAIL_ADDRESS": os.getenv("EMAIL_ADDRESS"),
            "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
        }
        for k, v in checks.items():
            icon = "✅" if v else "❌"
            color = "#22c55e" if v else "#ef4444"
            st.markdown(
                f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;'
                f'color:{color};padding:0.2rem 0;">{icon} {k}</div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.markdown('<div style="color:#f59e0b;font-size:0.8rem;">⚠️ .env not found</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-heading">Activity Log</div>', unsafe_allow_html=True)

    level_class = {"info": "log-info", "success": "log-success", "warn": "log-warn", "error": "log-error"}

    if not st.session_state.logs:
        log_html = '<div style="color:#475569;font-family:Space Mono,monospace;font-size:0.78rem;padding:0.5rem;">No activity yet. Start the agent to begin.</div>'
    else:
        entries = []
        for entry in list(st.session_state.logs)[-40:]:
            cls = level_class.get(entry["level"], "log-info")
            entries.append(
                f'<div class="log-entry">'
                f'<span class="log-time">[{entry["time"]}]</span>'
                f'<span class="{cls}">{entry["msg"]}</span>'
                f'</div>'
            )
        log_html = "\n".join(entries)

    st.markdown(f'<div class="log-container">{log_html}</div>', unsafe_allow_html=True)

# ── EMAIL HISTORY ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-heading">Recent Emails Processed</div>', unsafe_allow_html=True)

history = st.session_state.email_history
if not history:
    st.markdown(
        '<div style="color:#475569;font-size:0.85rem;padding:1rem 0;">No emails processed yet.</div>',
        unsafe_allow_html=True,
    )
else:
    for email in reversed(history[-10:]):
        replied_badge = '<span class="email-replied">✓ replied</span>' if email.get("replied") else ""
        st.markdown(f"""
        <div class="email-card">
            {replied_badge}
            <div class="email-sender">{email['sender']}</div>
            <div class="email-subject">{email['subject']}</div>
            <div class="email-time">{email['time']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Auto-refresh when running ─────────────────────────────────────────────────
if st.session_state.agent_running:
    time.sleep(5)
    st.rerun()
