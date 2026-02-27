"""
📧  email_reminder.py — Free email reminders via Gmail SMTP
Setup: Enable App Passwords at myaccount.google.com/apppasswords
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, ENABLE_EMAIL_REMINDERS, CLINIC_NAME, DOCTOR_NAME, CLINIC_LOCATION, CLINIC_PHONE


def send_reminder_email(to_email: str, patient_name: str, date: str, time: str, concern: str = ""):
    """Send appointment reminder email via Gmail (free)"""
    if not ENABLE_EMAIL_REMINDERS:
        print("📧 Email reminders disabled. Set ENABLE_EMAIL_REMINDERS=True in config.py")
        return False

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("❌ Gmail credentials missing in config.py")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Appointment Reminder — {date} at {time} | {CLINIC_NAME}"
        msg["From"]    = GMAIL_ADDRESS
        msg["To"]      = to_email

        html_body = f"""
        <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #2c7be5, #6f42c1); padding: 20px; border-radius: 12px; color: white; text-align: center;">
                <h2>🏥 {CLINIC_NAME}</h2>
                <p style="margin:0; opacity:0.9">Appointment Confirmation</p>
            </div>
            <div style="padding: 24px; background: #f9f9f9; border-radius: 0 0 12px 12px;">
                <p>Hi <strong>{patient_name}</strong>,</p>
                <p>Your appointment has been confirmed. Here are the details:</p>
                <div style="background: white; padding: 16px; border-radius: 10px; border-left: 4px solid #2c7be5; margin: 16px 0;">
                    <p>📅 <strong>Date:</strong> {date}</p>
                    <p>⏰ <strong>Time:</strong> {time}</p>
                    <p>👩‍⚕️ <strong>Doctor:</strong> {DOCTOR_NAME}</p>
                    <p>📍 <strong>Location:</strong> {CLINIC_LOCATION}</p>
                    <p>📞 <strong>Phone:</strong> {CLINIC_PHONE}</p>
                    {"<p>🩺 <strong>Concern:</strong> " + concern + "</p>" if concern else ""}
                </div>
                <p style="color: #555; font-size: 13px;">
                    ⚠️ Please arrive 10 minutes before your appointment.<br>
                    To reschedule or cancel, call us at {CLINIC_PHONE}.
                </p>
                <hr style="border: none; border-top: 1px solid #eee;">
                <p style="color: #999; font-size: 12px; text-align: center;">
                    This is an automated message from {CLINIC_NAME} AI Receptionist.
                </p>
            </div>
        </body></html>
        """

        text_body = f"""
Hi {patient_name},

Your appointment at {CLINIC_NAME} is confirmed.

📅 Date     : {date}
⏰ Time     : {time}
👩‍⚕️ Doctor   : {DOCTOR_NAME}
📍 Location : {CLINIC_LOCATION}
📞 Phone    : {CLINIC_PHONE}

Please arrive 10 minutes early.
To reschedule, call us at {CLINIC_PHONE}.

— {CLINIC_NAME} AI Receptionist
        """

        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body,  "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Reminder email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def send_cancellation_email(to_email: str, patient_name: str, date: str, time: str):
    """Send cancellation confirmation email"""
    if not ENABLE_EMAIL_REMINDERS:
        return False
    try:
        msg = MIMEText(f"""
Hi {patient_name},

Your appointment at {CLINIC_NAME} on {date} at {time} has been successfully cancelled.

To rebook, visit our chatbot or call {CLINIC_PHONE}.

— {CLINIC_NAME} AI Receptionist
        """)
        msg["Subject"] = f"Appointment Cancelled — {CLINIC_NAME}"
        msg["From"]    = GMAIL_ADDRESS
        msg["To"]      = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Cancellation email failed: {e}")
        return False
