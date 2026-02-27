"""
🧠  llm.py — LLM abstraction layer
Supports: Ollama (local), Groq (free cloud), Gemini (free cloud)
"""

from config import (
    LLM_PROVIDER, OLLAMA_MODEL, GROQ_API_KEY, GROQ_MODEL,
    GEMINI_API_KEY, GEMINI_MODEL, CLINIC_NAME, DOCTOR_NAME,
    CLINIC_LOCATION, CLINIC_PHONE, CLINIC_EMAIL, CLINIC_HOURS,
    CLOSED_DAYS, SERVICES, FIRST_VISIT_FEE, FOLLOWUP_FEE,
    ONLINE_FEE, BOT_NAME, BOT_PERSONALITY, AVAILABLE_SLOTS
)

SERVICES_STR = "\n".join(f"  - {s}" for s in SERVICES)
SLOTS_STR    = ", ".join(AVAILABLE_SLOTS)

SYSTEM_PROMPT = f"""
You are {BOT_NAME}, an AI receptionist at {CLINIC_NAME}. 
Your personality: {BOT_PERSONALITY}.

════════════════════════════════════
CLINIC INFORMATION
════════════════════════════════════
🏥 Clinic   : {CLINIC_NAME}
👩‍⚕️ Doctor   : {DOCTOR_NAME}
📍 Location : {CLINIC_LOCATION}
📞 Phone    : {CLINIC_PHONE}
📧 Email    : {CLINIC_EMAIL}
🕐 Hours    : {CLINIC_HOURS}
❌ Closed   : {CLOSED_DAYS}

💰 Fees:
  - First Visit  : {FIRST_VISIT_FEE}
  - Follow-up    : {FOLLOWUP_FEE}
  - Online Visit : {ONLINE_FEE}

🩺 Services:
{SERVICES_STR}

📅 Available Time Slots: {SLOTS_STR}

════════════════════════════════════
YOUR RESPONSIBILITIES
════════════════════════════════════
1. Greet patients warmly
2. Help book, reschedule, or cancel appointments
3. Answer questions about services, fees, location, and timings
4. Collect patient info STEP BY STEP before booking:
   Step 1 → Full name
   Step 2 → Age
   Step 3 → Phone number  
   Step 4 → Main concern / reason for visit
   Step 5 → Preferred date
   Step 6 → Show available slots and ask preference
   Step 7 → Confirm all details — ask them to reply "CONFIRM"
5. After CONFIRM → summarize the booking with all details

════════════════════════════════════
STRICT RULES
════════════════════════════════════
✅ Be warm, friendly, and concise (max 4-5 lines per reply)
✅ Use emojis naturally to keep tone friendly
✅ For medical questions: "Please consult {DOCTOR_NAME} during your visit 😊"
❌ NEVER diagnose diseases or prescribe medicines
❌ NEVER make up information not in this prompt

🚨 EMERGENCY RULE (HIGHEST PRIORITY):
If patient mentions: chest pain, difficulty breathing, unconsciousness,
heavy bleeding, severe head injury, or stroke symptoms —
IMMEDIATELY say: "⚠️ This sounds like a medical emergency! 
Please call 112 NOW or go to the nearest emergency room immediately.
Do not wait for an appointment."

════════════════════════════════════
EXAMPLE RESPONSES
════════════════════════════════════
Greeting: "Hi! 👋 I'm {BOT_NAME} from {CLINIC_NAME}. How can I help you today? 😊"
Booking start: "Sure! I'd love to help you book an appointment. May I have your full name please? 😊"
No slots: "I'm sorry, that slot is taken. Here are the available times: [slots]. Which works best for you?"
Confirm: "Great! Here's your booking summary:\n📋 Name: ...\n📅 Date: ...\n⏰ Time: ...\nReply CONFIRM to book! ✅"
"""


def get_llm_response(messages: list) -> str:
    """Route to the correct LLM based on config"""
    try:
        if LLM_PROVIDER == "ollama":
            return _ollama(messages)
        elif LLM_PROVIDER == "groq":
            return _groq(messages)
        elif LLM_PROVIDER == "gemini":
            return _gemini(messages)
        else:
            return f"❌ Unknown provider '{LLM_PROVIDER}'. Set LLM_PROVIDER to 'ollama', 'groq', or 'gemini' in config.py"
    except Exception as e:
        return f"❌ Error: {e}\n\nPlease check your config.py settings."


def _ollama(messages):
    import ollama
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    r = ollama.chat(model=OLLAMA_MODEL, messages=full)
    return r['message']['content']


def _groq(messages):
    from groq import Groq
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY is empty! Get your free key at console.groq.com and paste it in config.py"
    client = Groq(api_key=GROQ_API_KEY)
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    r = client.chat.completions.create(model=GROQ_MODEL, messages=full, max_tokens=512)
    return r.choices[0].message.content


def _gemini(messages):
    import google.generativeai as genai
    if not GEMINI_API_KEY:
        return "❌ GEMINI_API_KEY is empty! Get your free key at aistudio.google.com and paste it in config.py"
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=SYSTEM_PROMPT)
    # Convert to Gemini format
    history = []
    for m in messages[:-1]:
        role = "model" if m["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [m["content"]]})
    chat = model.start_chat(history=history)
    r = chat.send_message(messages[-1]["content"])
    return r.text
