"""
🏥 Clinic AI Receptionist — 100% Free
Uses: Ollama (local) or Groq/Gemini (free cloud API)
UI: Streamlit | DB: SQLite
"""

import streamlit as st
from datetime import datetime, date
from database import setup_db, get_appointments, get_slots, book_appointment
from llm import get_llm_response
from config import (
    CLINIC_NAME, DOCTOR_NAME, CLINIC_LOCATION, CLINIC_PHONE,
    CLINIC_HOURS, FIRST_VISIT_FEE, FOLLOWUP_FEE, BOT_NAME, AVAILABLE_SLOTS
)

# ─────────────────────────────────────────────
# 🎨  PAGE CONFIG
# ─────────────────────────────────────────────

def main():
    setup_db()

    st.set_page_config(
        page_title=f"{CLINIC_NAME}",
        page_icon="🏥",
        layout="wide"
    )

    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #2c7be5 0%, #6f42c1 100%);
        padding: 22px 30px; border-radius: 16px;
        color: white; margin-bottom: 20px;
    }
    .clinic-info-box {
        background: #f0f4ff; padding: 16px; border-radius: 12px;
        border-left: 5px solid #2c7be5; font-size: 14px; line-height: 1.9;
    }
    .appt-card {
        background: #e8f5e9; padding: 10px 14px; border-radius: 10px;
        border: 1px solid #a5d6a7; margin: 6px 0; font-size: 13px;
    }
    .slot-badge {
        display:inline-block; background:#d4edda; color:#155724;
        padding: 3px 10px; border-radius: 20px; font-size:13px; margin:3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h2 style="margin:0; font-size:26px">🏥 {CLINIC_NAME}</h2>
        <p style="margin:6px 0 0 0; opacity:0.85; font-size:15px">
            AI Receptionist &nbsp;|&nbsp; {BOT_NAME} is here to help you 😊
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2.2, 1])

    # ── LEFT: Chat ──────────────────────────────
    with col1:
        st.subheader("💬 Chat with " + BOT_NAME)

        if "messages" not in st.session_state:
            st.session_state.messages = []
            welcome = (
                f"Hi there! 👋 I'm **{BOT_NAME}**, your AI receptionist at **{CLINIC_NAME}**.\n\n"
                "I can help you:\n"
                "- 📅 **Book** an appointment\n"
                "- 🔄 **Reschedule or Cancel** an appointment\n"
                "- ❓ Answer questions about our **services, fees & location**\n\n"
                "How can I assist you today? 😊"
            )
            st.session_state.messages.append({"role": "assistant", "content": welcome})

        for msg in st.session_state.messages:
            avatar = "🤖" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Type your message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner(f"{BOT_NAME} is typing..."):
                    reply = get_llm_response(st.session_state.messages)
                st.markdown(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    # ── RIGHT: Info Panel ───────────────────────
    with col2:

        # Clinic Info
        st.markdown(f"""
        <div class="clinic-info-box">
            <b>🏥 {CLINIC_NAME}</b><br>
            👩‍⚕️ {DOCTOR_NAME}<br>
            📍 {CLINIC_LOCATION}<br>
            📞 {CLINIC_PHONE}<br>
            🕐 {CLINIC_HOURS}<br>
            💰 First Visit: <b>{FIRST_VISIT_FEE}</b><br>
            💰 Follow-up: <b>{FOLLOWUP_FEE}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick Buttons
        st.subheader("⚡ Quick Actions")

        def quick_msg(text):
            st.session_state.messages.append({"role": "user", "content": text})
            reply = get_llm_response(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("📅 Book Appointment",       use_container_width=True): quick_msg("I want to book an appointment")
        if st.button("❌ Cancel Appointment",      use_container_width=True): quick_msg("I want to cancel my appointment")
        if st.button("💰 Fees & Services",         use_container_width=True): quick_msg("What are the fees and services?")
        if st.button("🕐 Clinic Timings",          use_container_width=True): quick_msg("What are your clinic timings?")
        if st.button("📍 Location & Directions",   use_container_width=True): quick_msg("Where is the clinic and how do I get there?")
        if st.button("🔄 Clear Chat", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # Today's Appointments
        st.subheader("📋 Today's Bookings")
        today = date.today().strftime("%Y-%m-%d")
        appts = get_appointments(today)

        if appts:
            for a in appts:
                # a = (id, name, phone, age, concern, date, time, status)
                st.markdown(f"""
                <div class="appt-card">
                    ⏰ <b>{a[6]}</b> &nbsp;|&nbsp; {a[1]}<br>
                    📞 {a[2]}&nbsp; | 🩺 {str(a[4])[:35]}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No appointments booked today.")

        # Available Slots
        st.subheader("🟢 Open Slots Today")
        free_slots = get_slots(today, AVAILABLE_SLOTS)
        if free_slots:
            slots_html = "".join(f'<span class="slot-badge">{s}</span>' for s in free_slots)
            st.markdown(slots_html, unsafe_allow_html=True)
        else:
            st.warning("All slots are booked today!")

        st.markdown("---")

        # Manual Booking Form
        with st.expander("➕ Manually Add Appointment"):
            with st.form("manual_booking"):
                m_name    = st.text_input("Patient Name")
                m_phone   = st.text_input("Phone Number")
                m_age     = st.text_input("Age")
                m_concern = st.text_input("Concern / Reason")
                m_date    = st.date_input("Date", min_value=date.today())
                m_time    = st.selectbox("Time Slot", AVAILABLE_SLOTS)
                if st.form_submit_button("✅ Book Now"):
                    if m_name and m_phone and m_concern:
                        book_appointment(m_name, m_phone, m_age, m_concern,
                                         m_date.strftime("%Y-%m-%d"), m_time)
                        st.success(f"✅ Appointment booked for {m_name} on {m_date} at {m_time}!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields.")


if __name__ == "__main__":
    main()
