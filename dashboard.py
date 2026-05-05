import streamlit as st
import threading
import time
import queue
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #020408;
    color: #c9d1d9;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,255,180,0.015) 2px, rgba(0,255,180,0.015) 4px
    );
    pointer-events: none;
    z-index: 0;
}

.cyber-header {
    position: relative;
    padding: 1.5rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0,255,180,0.2);
}
.cyber-header::before {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 180px; height: 2px;
    background: linear-gradient(90deg, #00ffb4, transparent);
}
.cyber-title {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(0,255,180,0.4), 0 0 60px rgba(0,255,180,0.1);
}
.cyber-title span { color: #00ffb4; }
.cyber-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #00ffb4;
    letter-spacing: 0.15em;
    margin-top: 0.3rem;
    opacity: 0.7;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 1.1rem;
    border-radius: 3px;
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
}
.status-running {
    background: rgba(0,255,180,0.08);
    border: 1px solid rgba(0,255,180,0.5);
    color: #00ffb4;
    box-shadow: 0 0 20px rgba(0,255,180,0.15), inset 0 0 20px rgba(0,255,180,0.05);
}
.status-stopped {
    background: rgba(255,50,80,0.08);
    border: 1px solid rgba(255,50,80,0.4);
    color: #ff3250;
    box-shadow: 0 0 20px rgba(255,50,80,0.1);
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-green { background: #00ffb4; box-shadow: 0 0 8px #00ffb4, 0 0 16px #00ffb4; animation: blink 1.2s infinite; }
.dot-red { background: #ff3250; box-shadow: 0 0 8px #ff3250; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }

.metric-card {
    background: #0a0f1a;
    border: 1px solid rgba(0,255,180,0.15);
    border-top: 2px solid rgba(0,255,180,0.4);
    border-radius: 4px;
    padding: 1.2rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #00ffb4, transparent);
    opacity: 0.5;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: #00ffb4;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.6rem;
    opacity: 0.7;
}
.metric-value { font-family: 'Orbitron', monospace; font-size: 2.2rem; font-weight: 900; line-height: 1; }
.mv-blue  { color: #00b4ff; text-shadow: 0 0 20px rgba(0,180,255,0.5); }
.mv-green { color: #00ffb4; text-shadow: 0 0 20px rgba(0,255,180,0.5); }
.mv-red   { color: #ff3250; text-shadow: 0 0 20px rgba(255,50,80,0.5); }
.mv-gray  { color: #8b949e; font-size: 1.4rem; }

.section-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    color: #00ffb4;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.8rem;
    opacity: 0.6;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(0,255,180,0.3), transparent);
}

.log-wrap {
    background: #050a10;
    border: 1px solid rgba(0,255,180,0.12);
    border-left: 2px solid rgba(0,255,180,0.4);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.76rem;
    line-height: 1.8;
    max-height: 360px;
    overflow-y: auto;
}
.log-wrap::-webkit-scrollbar { width: 4px; }
.log-wrap::-webkit-scrollbar-track { background: #050a10; }
.log-wrap::-webkit-scrollbar-thumb { background: rgba(0,255,180,0.3); border-radius: 2px; }
.l-time { color: #30363d; margin-right: 0.6rem; }
.l-info    { color: #00b4ff; }
.l-success { color: #00ffb4; }
.l-warn    { color: #ffa500; }
.l-error   { color: #ff3250; }

.email-card {
    background: #050a10;
    border: 1px solid rgba(0,255,180,0.1);
    border-left: 3px solid #00ffb4;
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.e-sender  { font-weight: 600; color: #00ffb4; font-size: 0.88rem; font-family: 'Share Tech Mono', monospace; }
.e-subject { color: #8b949e; font-size: 0.8rem; margin-top: 0.2rem; }
.e-time    { color: #30363d; font-size: 0.72rem; font-family: 'Share Tech Mono', monospace; margin-top: 0.3rem; }
.e-badge {
    float: right; font-size: 0.65rem; padding: 0.1rem 0.5rem;
    background: rgba(0,255,180,0.1); border: 1px solid rgba(0,255,180,0.3);
    border-radius: 2px; color: #00ffb4;
    font-family: 'Orbitron', monospace; letter-spacing: 0.1em;
}

.stButton > button {
    border-radius: 3px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00ffb4, #00b4ff) !important;
    color: #020408 !important;
    box-shadow: 0 0 20px rgba(0,255,180,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 35px rgba(0,255,180,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    background: transparent !important;
    border: 1px solid rgba(0,255,180,0.3) !important;
    color: #00ffb4 !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: rgba(0,255,180,0.7) !important;
    box-shadow: 0 0 15px rgba(0,255,180,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
for key, default in [
    ("agent_running", False), ("emails_processed", 0), ("replies_sent", 0),
    ("errors", 0), ("logs", deque(maxlen=100)), ("email_history", []),
    ("agent_thread", None), ("stop_event", threading.Event()),
    ("log_queue", queue.Queue()), ("start_time", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Agent Logic ───────────────────────────────────────────────────────────────
def add_log(level, message, q):
    q.put({"time": datetime.now().strftime("%H:%M:%S"), "level": level, "msg": message})

def agent_loop(stop_event, log_queue, state_proxy):
    try:
        from config import validate_config, EMAIL_ADDRESS
        from email_utils import fetch_unread_emails, send_reply
        from ai_reply import generate_reply

        add_log("info", "⚙  Config validated. Connecting to Gmail...", log_queue)
        validate_config()
        add_log("success", f"✓  Connected as {EMAIL_ADDRESS}", log_queue)
        add_log("info", "◈  Agent loop started — polling every 30s", log_queue)

        while not stop_event.is_set():
            try:
                add_log("info", "▸  Checking inbox for unread emails...", log_queue)
                emails = fetch_unread_emails()
                if not emails:
                    add_log("info", "◌  No new emails. Waiting 30s...", log_queue)
                else:
                    for email_data in emails:
                        if stop_event.is_set():
                            break
                        sender  = email_data.get("sender", "unknown")
                        subject = email_data.get("subject", "(no subject)")
                        body    = email_data.get("body", "")
                        add_log("info", f"✉  Email from {sender} — {subject}", log_queue)
                        state_proxy["emails_processed"] += 1
                        try:
                            reply = generate_reply(body)
                            send_reply(sender, subject, reply)
                            add_log("success", f"✓  Reply sent to {sender}", log_queue)
                            state_proxy["replies_sent"] += 1
                            state_proxy["email_history"].append({
                                "sender": sender, "subject": subject,
                                "time": datetime.now().strftime("%H:%M:%S"), "replied": True,
                            })
                        except Exception as e:
                            add_log("error", f"✗  Failed to reply to {sender}: {e}", log_queue)
                            state_proxy["errors"] += 1
                stop_event.wait(30)
            except Exception as e:
                add_log("error", f"!  Loop error: {e}", log_queue)
                state_proxy["errors"] += 1
                stop_event.wait(10)
    except Exception as e:
        add_log("error", f"!!  Agent crashed: {e}", log_queue)
    add_log("warn", "■  Agent stopped.", log_queue)

# ── Sync state ────────────────────────────────────────────────────────────────
state_proxy = {
    "emails_processed": st.session_state.emails_processed,
    "replies_sent":     st.session_state.replies_sent,
    "errors":           st.session_state.errors,
    "email_history":    st.session_state.email_history,
}
while not st.session_state.log_queue.empty():
    st.session_state.logs.append(st.session_state.log_queue.get_nowait())
st.session_state.emails_processed = state_proxy["emails_processed"]
st.session_state.replies_sent     = state_proxy["replies_sent"]
st.session_state.errors           = state_proxy["errors"]

is_running    = st.session_state.agent_running
status_class  = "status-running" if is_running else "status-stopped"
dot_class     = "dot-green"      if is_running else "dot-red"
status_text   = "ONLINE"         if is_running else "OFFLINE"

# ── HEADER ────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown("""
    <div class="cyber-header">
        <div class="cyber-title">✉ EMAIL<span>-AI-</span>AGENT</div>
        <div class="cyber-subtitle">> AUTONOMOUS EMAIL AGENT</div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;align-items:center;height:100%;padding-top:1.2rem;">
        <div class="status-pill {status_class}">
            <span class="status-dot {dot_class}"></span>{status_text}
        </div>
    </div>""", unsafe_allow_html=True)

# ── METRICS ───────────────────────────────────────────────────────────────────
uptime = "—"
if st.session_state.start_time and is_running:
    secs = int(time.time() - st.session_state.start_time)
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    uptime = f"{h:02d}:{m:02d}:{s:02d}"

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Emails Processed</div><div class="metric-value mv-blue">{st.session_state.emails_processed}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Replies Sent</div><div class="metric-value mv-green">{st.session_state.replies_sent}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Errors</div><div class="metric-value mv-red">{st.session_state.errors}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">Uptime</div><div class="metric-value mv-gray">{uptime}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CONTROLS + LOG ────────────────────────────────────────────────────────────
left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="section-label">Controls</div>', unsafe_allow_html=True)
    if not is_running:
        if st.button("▶  START AGENT", use_container_width=True, type="primary"):
            st.session_state.stop_event    = threading.Event()
            st.session_state.emails_processed = 0
            st.session_state.replies_sent  = 0
            st.session_state.errors        = 0
            st.session_state.logs          = deque(maxlen=100)
            st.session_state.email_history = []
            st.session_state.start_time    = time.time()
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
        if st.button("■  STOP AGENT", use_container_width=True):
            st.session_state.stop_event.set()
            st.session_state.agent_running = False
            st.session_state.start_time    = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  REFRESH", use_container_width=True):
        st.rerun()

with right:
    st.markdown('<div class="section-label">Activity Log</div>', unsafe_allow_html=True)
    level_class = {"info": "l-info", "success": "l-success", "warn": "l-warn", "error": "l-error"}
    if not st.session_state.logs:
        log_html = '<span style="color:#30363d;">// no activity yet. start the agent to begin.</span>'
    else:
        rows = []
        for e in list(st.session_state.logs)[-40:]:
            cls = level_class.get(e["level"], "l-info")
            rows.append(f'<div><span class="l-time">[{e["time"]}]</span><span class="{cls}">{e["msg"]}</span></div>')
        log_html = "\n".join(rows)
    st.markdown(f'<div class="log-wrap">{log_html}</div>', unsafe_allow_html=True)

# ── EMAIL HISTORY ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Recent Emails Processed</div>', unsafe_allow_html=True)

history = st.session_state.email_history
if not history:
    st.markdown('<div style="color:#30363d;font-family:Share Tech Mono,monospace;font-size:0.8rem;padding:0.5rem 0;">// no emails processed yet.</div>', unsafe_allow_html=True)
else:
    for email in reversed(history[-10:]):
        badge = '<span class="e-badge">✓ SENT</span>' if email.get("replied") else ""
        st.markdown(f"""
        <div class="email-card">
            {badge}
            <div class="e-sender">{email['sender']}</div>
            <div class="e-subject">{email['subject']}</div>
            <div class="e-time">{email['time']}</div>
        </div>""", unsafe_allow_html=True)

# ── Auto-refresh ──────────────────────────────────────────────────────────────
if st.session_state.agent_running:
    time.sleep(5)
    st.rerun()
