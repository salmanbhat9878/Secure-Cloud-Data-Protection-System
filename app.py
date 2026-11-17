import streamlit as st
import re

from database import create_table, get_connection
from security import encrypt_data, decrypt_data
from access_control import (
    generate_capability_code,
    hash_capability_code,
    verify_capability_code
)


# Page configuration
st.set_page_config(
    page_title="Secure Cloud Data System",
    page_icon="🔐",
    layout="centered"
)


# Professional dark blue design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0F172A, #1E3A8A);
    color: #FFFFFF !important;
}

.stApp p,
.stApp label,
.stApp span,
.stMarkdown,
.stText,
.stCaption {
    color: #FFFFFF !important;
}

h1, h2, h3, h4 {
    color: #60A5FA !important;
}

input, textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

input::placeholder,
textarea::placeholder {
    color: #6B7280 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
}

.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1D4ED8 !important;
}

[data-testid="stDataFrame"] {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


# Activity logging function
def log_activity(activity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO activity_logs (activity) VALUES (?)",
        (activity,)
    )

    conn.commit()
    conn.close()


# IMPORTANT: Create all database tables before using them
create_table()


# Security Dashboard
st.divider()
st.subheader("📊 Security Dashboard")
st.caption("Live overview of secure data and access activity")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]
total_encrypted = total_users

cursor.execute("SELECT COUNT(*) FROM access_tokens")
total_tokens = cursor.fetchone()[0]

conn.close()


# Dashboard chart
st.write("### 📈 Data Security Overview")

st.bar_chart({
    "Records": [total_encrypted],
    "Capability Tokens": [total_tokens]
})


# Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Registered Users", total_users)

with col2:
    st.metric("🔐 Total Encrypted Records", total_encrypted)

with col3:
    st.metric("🔑 Active Capability Tokens", total_tokens)


# Security Activity Log
st.divider()
st.subheader("🛡️ Security Activity Log")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT activity, timestamp
    FROM activity_logs
    ORDER BY id DESC
    LIMIT 10
""")

activities = cursor.fetchall()
conn.close()

if activities:
    st.dataframe(
        [
            {"Activity": activity, "Time": timestamp}
            for activity, timestamp in activities
        ],
        use_container_width=True
    )
else:
    st.info("No security activities recorded yet.")


# Main application
st.divider()
st.title("🔐 Secure Cloud Data Protection")
st.subheader("🔑 Authorized Access Control")

if "capability_code" not in st.session_state:
    st.session_state.capability_code = None


# Generate Capability Code
if st.button("Generate Capability Code"):

    st.session_state.capability_code = generate_capability_code()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO access_tokens
        (username, token_hash)
        VALUES (?, ?)
        """,
        (
            "admin",
            hash_capability_code(st.session_state.capability_code)
        )
    )

    conn.commit()
    conn.close()

    log_activity("New admin capability code generated")

    st.success("Capability code generated!")


if st.session_state.capability_code:
    st.code(st.session_state.capability_code)

st.write("SQL Injection Protection + AES-256 Encryption")


# Register Secure User
st.subheader("📝 Register Secure User")

username = st.text_input("Enter Username")
password = st.text_input(
    "Encryption Password",
    type="password"
)
sensitive_data = st.text_area("Enter Sensitive Information")


if st.button("Securely Save Data"):

    if not username or not password or not sensitive_data:
        st.warning("Please fill all fields.")

    elif not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username):
        st.error("Invalid username format.")

    else:
        encrypted = encrypt_data(sensitive_data, password)

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (username, encrypted_data)
                VALUES (?, ?)
                """,
                (username, encrypted)
            )

            conn.commit()
            conn.close()

            log_activity(f"New user registered: {username}")

            st.success("User data securely saved!")

        except Exception:
            conn.close()
            st.error("Username already exists or database error.")


# Retrieve Secure Data
st.divider()
st.subheader("🔓 Retrieve Secure Data")

search_username = st.text_input(
    "Username for retrieval",
    key="search"
)

decrypt_password = st.text_input(
    "Encryption Password",
    type="password",
    key="decrypt"
)

capability_input = st.text_input(
    "Enter Capability Code",
    type="password",
    key="capability"
)


if st.button("Decrypt Data"):

    if not search_username or not decrypt_password or not capability_input:
        st.warning("Please fill all retrieval fields.")

    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT token_hash FROM access_tokens WHERE username = ?",
            ("admin",)
        )

        token_result = cursor.fetchone()
        conn.close()

        if not token_result or not verify_capability_code(
            capability_input,
            token_result[0]
        ):
            st.error("Invalid Capability Code.")
            log_activity("Rejected access attempt: invalid capability code")

        else:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT encrypted_data FROM users WHERE username = ?",
                (search_username,)
            )

            result = cursor.fetchone()
            conn.close()

            if result:
                try:
                    original = decrypt_data(
                        result[0],
                        decrypt_password
                    )

                    st.success("Decryption successful!")
                    st.write(original)

                    log_activity(
                        f"Data decrypted for user: {search_username}"
                    )

                except Exception:
                    st.error("Wrong password or invalid encrypted data.")
                    log_activity(
                        f"Failed decryption attempt for user: {search_username}"
                    )

            else:
                st.warning("User not found.")