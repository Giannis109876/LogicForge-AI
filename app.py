import streamlit as st
import sys
import subprocess

# Αυτόματο κατέβασμα της επίσημης βιβλιοθήκης της Groq
try:
    from groq import Groq
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    from groq import Groq

# 1. Ρύθμιση της σελίδας για επαγγελματικό σχεδιασμό (UI/UX)
st.set_page_config(page_title="LogicForge AI Pro", page_icon="⚙️", layout="centered")

# ΕΔΩ ΒΑΖΕΙΣ ΤΟ ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΣΟΥ ΚΛΕΙΔΙ (Αυτό που φτιάξαμε στην αρχή!)
# Αν δεν δουλεύει, βάλε ένα ολοκαίνουργιο κλειδί gsk_ από το Groq Cloud
GROQ_API_KEY = "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"

# Σχεδιασμός Αριστερής Μπάρας (Sidebar)
with st.sidebar:
    st.title("⚙️ LogicForge Pro")
    st.write("---")
    st.subheader("👑 Account Status")
    
    # Έλεγχος αν ο χρήστης έχει γράψει όνομα
    if "user_name" in st.session_state and st.session_state.user_name:
        st.success(f"👤 User: {st.session_state.user_name}")
        st.warning("⚠️ Plan: Free Trial (3 left)")
    else:
        st.error("👤 User: Not Logged In")
        
    st.write("---")
    st.subheader("☕ Support & Upgrade")
    st.markdown('[![Buy Me A Coffee](https://shields.io)](https://buymeacoffee.com)')
    st.write("---")
    st.caption("Version v3.0 (Premium Pro)\nPowered by Llama 3 (Ultra-Fast).")

# 2. ΣΥΣΤΗΜΑ LOGIN (Αναγνώριση Ονόματος)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.title("🔒 LogicForge AI - Secure Access")
    st.subheader("Welcome to the Forge. Please enter your name to unlock the AI.")
    
    name_input = st.text_input("Enter your name or nickname:", placeholder="e.g. John")
    if st.button("Unlock System 🔓"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            st.rerun()
        else:
            st.warning("Please enter a valid name.")
    st.stop() # Σταματάει τον κώδικα εδώ αν δεν έχει γίνει login!

# --- ΑΝ Ο ΧΡΗΣΤΗΣ ΕΧΕΙ ΚΑΝΕΙ LOGIN, ΒΛΕΠΕΙ ΤΑ ΠΑΡΑΚΑΤΩ ---

st.title("🧠 LogicForge AI Pro")
st.subheader(f"Welcome back, {st.session_state.user_name}. The machine is ready.")
st.write("---")

# 3. Σύστημα Μνήμης και Μετρητή Ερωτήσεων (Κόφτης Premium)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": f"You are a cold Logic Engineer. Ignore emotions. ALWAYS reply in the exact same language the user writes to you. Address the user by their name: {st.session_state.user_name}. Analyze everything exclusively based on logic, pros and cons, and provide a crystal clear, brutal, and realistic conclusion."
        }
    ]

if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# Εμφάνιση των προηγούμενων μηνυμάτων (Στυλ Chat)
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🧠"):
            st.write(message["content"])

# 4. Ο ΕΠΑΓΓΕΛΜΑΤΙΚΟΣ ΚΟΦΤΗΣ PREMIUM (Paywall)
if st.session_state.prompt_count >= 3:
    st.error("🚨 PREMIUM LOCK ACTIVE")
    st.info(f"⚡ {st.session_state.user_name}, you have used all 3 free daily analyses allowed for Free accounts. Upgrade to Pro to unlock unlimited access to the ultra-fast Llama 3 engine.")
    st.button("💎 Upgrade to Premium Pro ($4.99/mo)", disabled=True)
else:
    # Αν δεν έχει φτάσει το όριο, το chat είναι ανοιχτό!
    if user_input := st.chat_input("Type your dilemma or question here..."):
        
        # Αυξάνουμε τον μετρητή κατά 1
        st.session_state.prompt_count += 1
        
        with st.chat_message("user"):
            st.write(user_input)
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant", avatar="🧠"):
            message_placeholder = st.empty()
            message_placeholder.write("🧠 High-speed engine is processing data...")
            
            try:
                # Σύνδεση με το επίσημο, υπερ-σταθερό Groq API
                client = Groq(api_key=GROQ_API_KEY)
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama3-8b-8192", # Το πιο γρήγορο και έξυπνο μοντέλο ανοιχτού κώδικα
                )
                response = chat_completion.choices.message.content
                message_placeholder.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun() # Ανανέωση για να αλλάξει ο μετρητής στο Sidebar live!
            except Exception as e:
                message_placeholder.write("An authentication error occurred. Please make sure your Groq API Key is valid.")

st.write("---")
# Οι 3 Κάρτες «Εγγύησης»
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

