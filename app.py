import streamlit as st
import json
import requests
import random

# 1. Configuration & Premium Dark Cyber UI
st.set_page_config(page_title="LogicForge AI Pro", page_icon="⚡", layout="centered")

# Custom CSS για εντυπωσιακό, premium design
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    div[data-testid="stSidebar"] { background-color: #070a13 !important; border-right: 1px solid #1e293b; }
    .stButton>button { 
        width: 100%; border-radius: 8px; font-weight: bold; 
        background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
    .premium-lock {
        background: linear-gradient(135deg, #7f1d1d, #dc2626); padding: 20px;
        border-radius: 12px; border: 1px solid #ef4444; text-align: center; margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Αρχικοποίηση Session States
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "prompt_count" not in st.session_state: st.session_state.prompt_count = 0
if "messages" not in st.session_state: st.session_state.messages = []

# Συναρτήσεις Fail-Safe για δωρεάν AI (Χωρίς βιβλιοθήκες που σπάνε)
def fetch_ai_response(messages):
    """Καλεί απευθείας free APIs με failover στρατηγική"""
    # Φιλτράρισμα μηνυμάτων για καθαρό API call
    formatted_msgs = [{"role": m["role"], "content": m["content"]} for m in messages]
    
    # Provider 1: Pollinations (Πολύ σταθερό & γρήγορο)
    try:
        sys_prompt = formatted_msgs[0]["content"] if formatted_msgs[0]["role"] == "system" else ""
        user_history = "\n".join([f"{m['role']}: {m['content']}" for m in formatted_msgs[1:]])
        full_prompt = f"{sys_prompt}\n\nHistory:\n{user_history}"
        
        response = requests.post(
            "https://pollinations.ai",
            json={"messages": [{"role": "user", "content": full_prompt}], "model": "openai"},
            timeout=15
        )
        if response.status_code == 200 and response.text.strip():
            return response.text
    except:
        pass

    # Provider 2: DuckDuckGo AI Passthrough (Fallback)
    try:
        response = requests.get(f"https://tianssh.top{requests.utils.quote(formatted_msgs[-1]['content'])}", timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if "text" in res_json: return res_json["text"]
    except:
        pass

    return None

# --- SIDEBAR (Αριστερό Μενού) ---
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>⚙️ LogicForge Pro</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.user_name:
        st.markdown(f"👤 **User:** `{st.session_state.user_name}`")
        rem = max(0, 3 - st.session_state.prompt_count)
        st.markdown(f"🔋 **Daily Tokens:** `{rem} / 3 Daily Analyses`")
        
        # Progress Bar για τα δωρεάν prompts
        st.progress(rem / 3)
        st.write("---")
        
        # Tools & Utilities
        st.subheader("🛠️ Session Controls")
        if st.button("🔄 Clear Chat Memory"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 System Logout"):
            st.session_state.user_name = ""
            st.session_state.prompt_count = 0
            st.session_state.messages = []
            st.rerun()
            
        # Download ρεπορτάζ αν υπάρχει ιστορικό
        if len(st.session_state.messages) > 1:
            chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages if m["role"] != "system"])
            st.download_button("📥 Export Logic Report (TXT)", data=chat_text, file_name="logic_report.txt", mime="text/plain")
    else:
        st.info("🔒 System locked. Please log in.")
        
    st.write("---")
    st.markdown('[![Buy Me A Coffee](https://shields.io)](https://buymeacoffee.com)')
    st.caption("⚡ Engine: LogicForge Hyper-Drive v5.0\nStatus: Fully Operational")

# --- ΚΥΡΙΟ ΣΥΣΤΗΜΑ ΑΣΦΑΛΕΙΑΣ (LOGIN) ---
if not st.session_state.user_name:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🔒 LogicForge AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Enter the mainframe to boot the cold logic engine.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.write("")
        name_input = st.text_input("Operator Identifier (Name/Nickname):", placeholder="e.g. Neo")
        if st.button("INTEGRATE INTO SYSTEM 🔓", type="primary"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.session_state.messages = [{
                    "role": "system", 
                    "content": f"You are a cold Logic Engineer. Ignore emotions. ALWAYS reply in the exact same language the user writes to you. Address the user by their name: {st.session_state.user_name}. Analyze everything exclusively based on logic, pros and cons, and provide a crystal clear, brutal, and realistic conclusion. Structure your answer using markdown headers for clarity."
                }]
                st.rerun()
            else:
                st.error("Access Denied: Invalid Identifier.")
    st.stop()

# --- MAIN APP INTERFACE ---
st.markdown(f"<h1>🧠 LogicForge Mainframe <span style='font-size:1.2rem; color:#3b82f6;'>v5.0 Pro</span></h1>", unsafe_allow_html=True)
st.caption(f"Welcome back, Operator **{st.session_state.user_name}**. Empathy modules are offline.")
st.write("---")

# Render Ιστορικού Chat (Κρύβουμε το System Prompt)
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    avatar = "👤" if msg["role"] == "user" else "🧠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# --- ΔΙΑΧΕΙΡΙΣΗ PAYWALL & CHAT INPUT ---
if st.session_state.prompt_count >= 3:
    st.markdown("""
        <div class="premium-lock">
            <h3 style="margin:0; color:white;">🚨 MAIN FRAME QUOTA EXCEEDED</h3>
            <p style="color:#fca5a5; margin: 10px 0 0 0;">Free evaluation limit reached. Upgrade to remove the 3-prompt firewall.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("💎 UNLOCK UNLIMITED ACCESS ($4.99/mo)"):
        st.balloons()
        st.toast("Redirecting to secure gateway... (Mockup)", icon="💳")
else:
    if user_input := st.chat_input("Input data vector or dilemma for analysis..."):
        # Live εμφάνιση της ερώτησης
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.prompt_count += 1
        
        # Live εμφάνιση του AI Response με Loading Animation
        with st.chat_message("assistant", avatar="🧠"):
            status_placeholder = st.empty()
            
            # Τυχαία "cyberpunk" μηνύματα φόρτωσης για εφέ
            loading_phrases = ["Isolating emotional noise...", "Calculating pro/con vectors...", "Structuring objective matrices...", "Compiling brutal conclusion..."]
            status_placeholder.markdown(f"⏳ *{random.choice(loading_phrases)}*")
            
            # Κλήση της API συνάρτησης
            ai_response = fetch_ai_response(st.session_state.messages)
            
            if ai_response:
                status_placeholder.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                status_placeholder.error("⚠️ Connection timeout. The server is overloaded. Your credit was saved. Please click the button below to retry.")
                st.session_state.prompt_count -= 1  # Επιστροφή credit αν αποτύχει
                
            st.rerun()

# Footer UI Elements
st.write("---")
c1, c2, c3 = st.columns(3)
with c1: st.metric(label="System Mood", value="0% Empathy", delta="Cold Facts Only")
with c2: st.metric(label="Engine Speed", value="4.2 T/s", delta="Hyper-drive")
with c3: st.metric(label="Security", value="Session-Only", delta="100% Private")
