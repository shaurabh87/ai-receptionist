import streamlit as st
import os

# Reads secret from Streamlit Cloud (or local secrets.toml)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

"""
⚙️  config.py — Edit ALL your clinic settings here
"""

# ─────────────────────────────────────────────────────────────
# 🤖  LLM PROVIDER — Choose ONE
# ─────────────────────────────────────────────────────────────
# "ollama"  → Free, runs on YOUR computer (needs Ollama installed)
# "groq"    → Free cloud API, no GPU needed (get key: console.groq.com)
# "gemini"  → Free cloud API, no GPU needed (get key: aistudio.google.com)

LLM_PROVIDER   = "groq"          # Change to "groq" or "gemini"

OLLAMA_MODEL   = "llama3"          # After: ollama pull llama3
                                   # Other options: mistral, phi3, gemma

GROQ_API_KEY   = ""                # Paste your free Groq API key here
GROQ_MODEL     = "llama-3.1-8b-instant"  # Free model on Groq

GEMINI_API_KEY = ""                # Paste your free Gemini API key here
GEMINI_MODEL   = "gemini-1.5-flash" # Free model on Google AI Studio

# ─────────────────────────────────────────────────────────────
# 🏥  CLINIC DETAILS — Edit these!
# ─────────────────────────────────────────────────────────────
CLINIC_NAME     = "Dr. Priya's Wellness & Diet Clinic"
DOCTOR_NAME     = "Dr. Priya Sharma"
SPECIALIZATION  = "Nutritionist & Dietician"
CLINIC_LOCATION = "45 Green Avenue, Koregaon Park, Pune, Maharashtra"
CLINIC_PHONE    = "+91 98765 43210"
CLINIC_EMAIL    = "drpriya@clinic.com"
CLINIC_HOURS    = "Monday to Saturday, 10:00 AM – 7:00 PM"
CLOSED_DAYS     = "Sundays and National Holidays"

# ─────────────────────────────────────────────────────────────
# 💰  FEES
# ─────────────────────────────────────────────────────────────
FIRST_VISIT_FEE = "₹500"
FOLLOWUP_FEE    = "₹300"
ONLINE_FEE      = "₹400"

# ─────────────────────────────────────────────────────────────
# 🩺  SERVICES
# ─────────────────────────────────────────────────────────────
SERVICES = [
    "Diet Consultation",
    "Weight Loss Program",
    "Weight Gain Program",
    "Diabetes Diet Plan",
    "PCOS / PCOD Diet",
    "Thyroid Diet Plan",
    "Child & Infant Nutrition",
    "Sports Nutrition",
    "Pregnancy Diet",
    "Heart Healthy Diet",
]

# ─────────────────────────────────────────────────────────────
# 📅  APPOINTMENT SLOTS
# ─────────────────────────────────────────────────────────────
AVAILABLE_SLOTS = [
    "10:00 AM", "11:00 AM", "12:00 PM",
    "2:00 PM",  "3:00 PM",  "4:00 PM",
    "5:00 PM",  "6:00 PM"
]

# ─────────────────────────────────────────────────────────────
# 🤖  BOT PERSONA
# ─────────────────────────────────────────────────────────────
BOT_NAME        = "Aria"
BOT_PERSONALITY = "warm, professional, empathetic, concise"

# ─────────────────────────────────────────────────────────────
# 📧  EMAIL REMINDERS (Gmail SMTP — Free)
# ─────────────────────────────────────────────────────────────
# Enable Gmail App Password at: myaccount.google.com/apppasswords
ENABLE_EMAIL_REMINDERS = False     # Set True after configuring below
GMAIL_ADDRESS          = ""        # e.g. "yourclinic@gmail.com"
GMAIL_APP_PASSWORD     = ""        # 16-char Gmail App Password (not your login password)
