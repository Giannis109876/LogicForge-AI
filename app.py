import streamlit as st
import sys
import subprocess

# 1. Αυτόματο κατέβασμα της ελεύθερης βιβλιοθήκης αν δεν υπάρχει
try:
    import g4f
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "g4f"])
    import g4f

# 2. Ρύθμιση της σελίδας για επαγγελματικό σχεδιασμό (UI/UX)
st.set_page_config(page_title="LogicForge AI", page_icon="🧠", layout="centered")

# Σχεδιασμός Αριστερής Μπάρας (Sidebar) στα Αγγλικά
with st.sidebar:
    st.title("⚙️ LogicForge AI")
    st.write("---")
    st.subheader("🛠️ Forge Tools")
    st.info("🎯 New Dilemma Analysis")
    st.write("---")
    st.caption("Version v2.0 (Stable)\nBased 100% on Logic.")

# Κεντρικός Τίτλος και Μήνυμα Καλωσορίσματος στα Αγγλικά
st.title("🧠 LogicForge AI")
st.subheader("The cold engineer that forges your data into clear decisions.")
st.write("---")

st.info("👋 Welcome! There is no room for emotions, anxiety, or excuses here. I analyze everything exclusively based on cold logic and hard data.")

# 3. Σύστημα Μνήμης (Session State) - Το AI απαντάει στη γλώσσα του χρήστη!
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are a cold Logic Engineer. Ignore emotions. ALWAYS reply in the exact same language the user writes to you. Analyze everything exclusively based on logic, pros and cons, and provide a crystal clear, brutal, and realistic conclusion. Remember all previous messages in the chat history."
        }
    ]

# 4. Εμφάνιση των προηγούμενων μηνυμάτων (Στυλ Chat)
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🧠"):
            st.write(message["content"])

# 5. Είσοδος Νέου Μηνύματος (Το κουτί chat στο κάτω μέρος της οθόνης)
if user_input := st.chat_input("Type your dilemma or question here..."):
    
    # Εμφανίζουμε το μήνυμα του χρήστη
    with st.chat_message("user"):
        st.write(user_input)
        
    # Το αποθηκεύουμε στη μνήμη
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Σύνδεση με το AI και απάντηση
    with st.chat_message("assistant", avatar="🧠"):
        message_placeholder = st.empty()
        message_placeholder.write("Cold logic is processing your data...")
        
        try:
            # Στέλνουμε όλο το ιστορικό της μνήμης στον αναβαθμισμένο server
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            
            # Εμφανίζουμε την απάντηση
            message_placeholder.write(response)
            
            # Αποθηκεύουμε την απάντηση στη μνήμη
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            # Αν κολλήσει ο gpt-4o, δοκιμάζει αυτόματα εναλλακτικό server
            try:
                response = g4f.ChatCompletion.create(
                    model="llama-3.1-70b",
                    messages=st.session_state.messages
                )
                message_placeholder.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e2:
                message_placeholder.write("Free servers are temporarily busy. Please retry in a few seconds.")

st.write("---")

# 6. Οι 3 Κάρτες «Εγγύησης» στα Αγγλικά (Όπως στο ChatGPT)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("❄️ Zero Emotion")
    st.caption("We ignore anxiety, fear, and excuses. We focus only on the cold, hard truth.")

with col2:
    st.subheader("📐 Engineer Structure")
    st.caption("We break down every complex dilemma into clear logical steps, pros, and cons.")

with col3:
    st.subheader("🔒 Absolute Control")
    st.caption("The code protects you. You provide the data, and you drive the machine completely.")
