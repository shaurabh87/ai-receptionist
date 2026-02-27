"""
🗄️  database.py — SQLite appointment management (100% free, no setup needed)
"""

import sqlite3
from datetime import datetime

DB_FILE = "clinic_appointments.db"


def setup_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            phone      TEXT NOT NULL,
            age        TEXT,
            concern    TEXT,
            date       TEXT NOT NULL,
            time       TEXT NOT NULL,
            status     TEXT DEFAULT 'confirmed',
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT,
            phone      TEXT UNIQUE,
            age        TEXT,
            email      TEXT,
            notes      TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def book_appointment(name, phone, age, concern, date, time):
    """Save a new appointment"""
    conn = sqlite3.connect(DB_FILE)
    # Check if slot is already taken
    taken = conn.execute(
        "SELECT id FROM appointments WHERE date=? AND time=? AND status='confirmed'",
        (date, time)
    ).fetchone()

    if taken:
        conn.close()
        return False, f"❌ Slot {time} on {date} is already booked. Please choose another time."

    conn.execute(
        "INSERT INTO appointments (name,phone,age,concern,date,time,created_at) VALUES (?,?,?,?,?,?,?)",
        (name, phone, age, concern, date, time, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return True, f"✅ Appointment confirmed for {name} on {date} at {time}!"


def get_appointments(date=None):
    """Get all appointments, optionally filtered by date"""
    conn = sqlite3.connect(DB_FILE)
    if date:
        rows = conn.execute(
            "SELECT * FROM appointments WHERE date=? AND status='confirmed' ORDER BY time",
            (date,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM appointments WHERE status='confirmed' ORDER BY date, time"
        ).fetchall()
    conn.close()
    return rows


def get_slots(date, all_slots):
    """Return list of available (unbooked) slots for a date"""
    conn = sqlite3.connect(DB_FILE)
    booked = [r[0] for r in conn.execute(
        "SELECT time FROM appointments WHERE date=? AND status='confirmed'", (date,)
    ).fetchall()]
    conn.close()
    return [s for s in all_slots if s not in booked]


def cancel_appointment(name, phone):
    """Cancel appointment by patient name and phone"""
    conn = sqlite3.connect(DB_FILE)
    appt = conn.execute(
        "SELECT * FROM appointments WHERE name=? AND phone=? AND status='confirmed' ORDER BY date DESC LIMIT 1",
        (name, phone)
    ).fetchone()

    if not appt:
        conn.close()
        return False, "❌ No confirmed appointment found for this name and phone number."

    conn.execute(
        "UPDATE appointments SET status='cancelled' WHERE id=?", (appt[0],)
    )
    conn.commit()
    conn.close()
    return True, f"✅ Appointment for {name} on {appt[5]} at {appt[6]} has been cancelled."


def reschedule_appointment(name, phone, new_date, new_time):
    """Reschedule an existing appointment"""
    conn = sqlite3.connect(DB_FILE)
    appt = conn.execute(
        "SELECT * FROM appointments WHERE name=? AND phone=? AND status='confirmed' ORDER BY date DESC LIMIT 1",
        (name, phone)
    ).fetchone()

    if not appt:
        conn.close()
        return False, "❌ No confirmed appointment found."

    # Check new slot availability
    taken = conn.execute(
        "SELECT id FROM appointments WHERE date=? AND time=? AND status='confirmed'",
        (new_date, new_time)
    ).fetchone()

    if taken:
        conn.close()
        return False, f"❌ Slot {new_time} on {new_date} is already taken."

    conn.execute(
        "UPDATE appointments SET date=?, time=? WHERE id=?",
        (new_date, new_time, appt[0])
    )
    conn.commit()
    conn.close()
    return True, f"✅ Appointment rescheduled to {new_date} at {new_time}!"


def get_patient_history(phone):
    """Get all past appointments for a patient"""
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT * FROM appointments WHERE phone=? ORDER BY date DESC", (phone,)
    ).fetchall()
    conn.close()
    return rows
