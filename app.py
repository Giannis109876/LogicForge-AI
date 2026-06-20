import streamlit as st
import requests

# 1. Configuration & UI Setup
st.set_page_config(page_title="LogicForge AI Pro", page_icon="⚡", layout="centered")

# Επιβολή Dark Theme στα βασικά στοιχεία
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19 !important; color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] { background-color: #070a13 !important; border-right: 1px solid #1e293b; }
    .stButton>button { 
        width: 100%; border-radius: 8px; font-weight: bold; 
        background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; border: none;
    }
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

# Συναρτήση AI - Νέο σταθερό API Endpoint που δεν μπλοκάρει το Streamlit Cloud
def fetch_ai_response(messages_list):
    try:
        last_user_query = ""
        for m in reversed(messages_list):
            if m["role"] == "user":
                last_user_query = m["content"]
                break
        
        # Σκληρές οδηγίες για τον Cold Logic Engineer
        system_rules = f"You are a cold Logic Engineer. Ignore emotions. Answer strictly in GREEK. Address the user by name: {st.session_state.user_name}. Provide a clear analysis with pros, cons, and a brutal realistic conclusion."
        full_query = f"{system_rules}\n\nUser Question: {last_user_query}"
        
        # Χρήση εναλλακτικού ελεύθερου API Gateway (Cloudflare-friendly passthrough)
        url = f"https://tianssh.top{requests.utils.quote(full_query)}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            if "text" in res_json and res_json["text"].strip():
                return res_json["text"]
    except Exception:
        pass
    return "⚠️ Τα δωρεάν κανάλια επικοινωνίας είναι προσωρινά γεμάτα λόγω αυξημένης κίνησης. Δοκίμασε να ξαναστείλεις το μήνυμα σε 5 δευτερόλεπτα."

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>⚙️ LogicForge Pro</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.user_name:
        st.markdown(f"👤 **User:** `{st.session_state.user_name}`")
        rem = max(0, 3 - st.session_state.prompt_count)
        st.markdown(f"🔋 **Daily Tokens:** `{rem} / 3 Daily Analyses`")
        st.progress(rem / 3)
        st.write("---")
        
        st.subheader("🛠️ Session Controls")
        if st.button("🔄 Clear Chat Memory"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("🚪 System Logout"):
            st.session_state.user_name = ""
            st.session_state.prompt_count = 0
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("🔒 System locked. Please log in.")

# --- LOGIN SCREEN ---
if not st.session_state.user_name:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🔒 LogicForge AI</h1>", unsafe_allow_html=True)
    name_input = st.text_input("Operator Identifier:", placeholder="e.g. John")
    if st.button("INTEGRATE 🔓", type="primary"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            st.rerun()
    st.stop()

# --- MAIN INTERFACE ---
st.markdown(f"<h1>🧠 LogicForge Mainframe <span style='font-size:1.2rem; color:#3b82f6;'>v5.0 Pro</span></h1>", unsafe_allow_html=True)
st.write("---")

# Εμφάνιση μηνυμάτων με Custom HTML για εγγυημένα σωστά Dark Χρώματα
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div style='background-color: #1e293b; padding: 14px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #334155;'>
                <b style='color: #3b82f6;'>👤 {st.session_state.user_name}:</b><br><span style='color: #e2e8f0;'>{msg['content']}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #111827; padding: 14px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b;'>
                <b style='color: #10b981;'>🧠 LogicForge AI:</b><br><span style='color: #e2e8f0;'>{msg['content']}</span>
            </div>
        """, unsafe_allow_html=True)

# --- CHAT INPUT & PAYWALL ---
if st.session_state.prompt_count >= 3:
    st.markdown("""
        <div class="premium-lock">
            <h3 style="margin:0; color:white;">🚨 QUOTA EXCEEDED</h3>
            <p style="color:#fca5a5;">Upgrade to Pro to remove the firewall.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    if user_input := st.chat_input("Input data vector for analysis..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.prompt_count += 1
        
        with st.spinner("⏳ Analyzing vectors..."):
            ai_response = fetch_ai_response(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        st.rerun()
