import streamlit as st
import sys
import subprocess

# Αυτόματο κατέβασμα της βιβλιοθήκης αν δεν υπάρχει
try:
    import g4f
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "g4f"])
    import g4f

# 1. Ρύθμιση της σελίδας (UI/UX)
st.set_page_config(page_title="LogicForge AI Pro", page_icon="⚙️", layout="centered")

# Αρχικοποίηση μεταβλητών στο session_state
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# Σχεδιασμός Αριστερής Μπάρας (Sidebar)
with st.sidebar:
    st.title("⚙️ LogicForge Pro")
    st.write("---")
    st.subheader("👑 Account Status")
    if st.session_state.user_name:
        st.success(f"👤 User: {st.session_state.user_name}")
        remaining = max(0, 3 - st.session_state.prompt_count)
        st.warning(f"⚠️ Plan: Free Trial ({remaining} left)")
    else:
        st.error("👤 User: Not Logged In")
    st.write("---")
    st.subheader("☕ Support & Upgrade")
    st.markdown('[![Buy Me A Coffee](https://shields.io)](https://buymeacoffee.com)')
    st.write("---")
    st.caption("Version v3.5 (Premium Pro)\nPowered by Free Engines.")

# 2. ΣΥΣΤΗΜΑ LOGIN
if not st.session_state.user_name:
    st.title("🔒 LogicForge AI - Secure Access")
    st.subheader("Welcome to the Forge. Please enter your name to unlock the AI.")
    name_input = st.text_input("Enter your name or nickname:", placeholder="e.g. John")
    if st.button("Unlock System 🔓"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            # Ορισμός του αρχικού system prompt μόλις γίνει το login
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": f"You are a cold Logic Engineer. Ignore emotions. ALWAYS reply in the exact same language the user writes to you. Address the user by their name: {st.session_state.user_name}. Analyze everything exclusively based on logic, pros and cons, and provide a crystal clear, brutal, and realistic conclusion. Remember all previous messages."
                }
            ]
            st.rerun()
        else:
            st.warning("Please enter a valid name.")
    st.stop()

# --- ΑΝ Ο ΧΡΗΣΤΗΣ ΕΧΕΙ ΚΑΝΕΙ LOGIN ---
st.title("🧠 LogicForge AI Pro")
st.subheader(f"Welcome back, {st.session_state.user_name}. The machine is ready.")
st.write("---")

# Εμφάνιση προηγούμενων μηνυμάτων (παραλείποντας το system prompt)
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🧠"):
            st.write(message["content"])

# 3. Ο ΚΟΦΤΗΣ PREMIUM (Paywall)
if st.session_state.prompt_count >= 3:
    st.error("🚨 PREMIUM LOCK ACTIVE")
    st.info(f"⚡ {st.session_state.user_name}, you have used all 3 free daily analyses allowed for Free accounts.")
    st.button("💎 Upgrade to Premium Pro ($4.99/mo)", disabled=True)
else:
    # Λήψη ερώτησης χρήστη
    if user_input := st.chat_input("Type your dilemma or question here..."):
        # Εμφάνιση του μηνύματος του χρήστη άμεσα
        with st.chat_message("user"):
            st.write(user_input)
        
        # Αποθήκευση στη μνήμη
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.prompt_count += 1
        
        # Δημιουργία placeholder για την απάντηση του AI
        with st.chat_message("assistant", avatar="🧠"):
            message_placeholder = st.empty()
            message_placeholder.write("🧠 High-speed free engine is processing data...")
            
            response = ""
            # Προσπάθεια 1: gpt-4o
            try:
                client = g4f.client.Client()
                api_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                response = api_response.choices[0].message.content
            except Exception:
                # Προσπάθεια 2: llama-3.1-70b αν αποτύχει η πρώτη
                try:
                    client = g4f.client.Client()
                    api_response = client.chat.completions.create(
                        model="llama-3.1-70b",
                        messages=st.session_state.messages
                    )
                    response = api_response.choices[0].message.content
                except Exception:
                    response = "Free servers are temporarily busy. Please retry in a few seconds."

            # Εμφάνιση της τελικής απάντησης
            message_placeholder.write(response)
            
            # Αποθήκευση της απάντησης στη μνήμη
            st.session_state.messages.append({"role": "assistant", "content": response})

st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("❄️ Zero Emotion")
    st.caption("We focus only on the cold, hard truth.")
with col2:
    st.subheader("📐 Engineer Structure")
    st.caption("Clear logical steps, pros, and cons.")
with col3:
    st.subheader("🔒 Absolute Control")
    st.caption("The code protects you. You drive the machine.")
