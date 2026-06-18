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

# Σχεδιασμός Αριστερής Μπάρας (Sidebar) όπως στην εικόνα
with st.sidebar:
    st.title("⚙️ LogicForge AI")
    st.write("---")
    st.subheader("🛠️ Εργαλεία Σφυρηλάτησης")
    st.info("🎯 Νέα Ανάλυση Διλήμματος")
    st.write("---")
    st.caption("Έκδοση v2.0 (Stable)\nΒασισμένο 100% στη Λογική.")

# Κεντρικός Τίτλος και Μήνυμα Καλωσορίσματος
st.title("🧠 LogicForge AI")
st.subheader("Ο ψυχρός μηχανικός που σφυρηλατεί τα δεδομένα σου σε καθαρές αποφάσεις.")
st.write("---")

st.info("👋 Καλωσήρθες! Εδώ δεν υπάρχουν συναισθήματα, άγχος ή δικαιολογίες. Αναλύω τα πάντα αποκλειστικά με βάση την ψυχρή λογική και τα δεδομένα.")

# 3. Σύστημα Μνήμης (Session State) για να θυμάται τη συζήτηση
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Είσαι ένας ψυχρός Μηχανικός Λογικής. Αγνοείς τα συναισθήματα. Απαντάς πάντα στα ελληνικά. Αναλύεις τα πάντα αποκλειστικά με βάση τη λογική, τα υπέρ και τα κατά, και βγάζεις ένα ξεκάθαρο, ωμό και ρεαλιστικό συμπέρασμα. Θυμάσαι όλες τις προηγούμενες γραμμές της συζήτησης και χτίζεις πάνω σε αυτές."
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
if user_input := st.chat_input("Γράψε το δίλημμα ή την ερώτησή σου εδώ..."):
    
    # Εμφανίζουμε το μήνυμα του χρήστη
    with st.chat_message("user"):
        st.write(user_input)
        
    # Το αποθηκεύουμε στη μνήμη
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Σύνδεση με το AI και απάντηση
    with st.chat_message("assistant", avatar="🧠"):
        message_placeholder = st.empty()
        message_placeholder.write("Η ψυχρή λογική επεξεργάζεται τα δεδομένα σου...")
        
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
                message_placeholder.write("Οι δωρεάν servers είναι προσωρινά γεμάτοι. Παρακαλώ ξαναπροσπάθησε σε λίγα δευτερόλεπτα.")

st.write("---")

# 6. Οι 3 Κάρτες «Εγγύησης» στο κάτω μέρος (Όπως στην εικόνα του ChatGPT)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("❄️ Μηδέν Συναίσθημα")
    st.caption("Αγνοούμε το άγχος, τον φόβο και τις δικαιολογίες. Εστιάζουμε μόνο στην ψυχρή αλήθεια.")

with col2:
    st.subheader("📐 Δομή Μηχανικού")
    st.caption("Σπάμε κάθε σύνθετο δίλημμα σε ξεκάθαρα λογικά βήματα, πλεονεκτήματα και μειονεκτήματα.")

with col3:
    st.subheader("🔒 Απόλυτος Έλεγχος")
    st.caption("Ο κώδικας σε προστατεύει. Εσύ δίνεις τα δεδομένα και εσύ κατευθύνεις απόλυτα τη μηχανή.")
