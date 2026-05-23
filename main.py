# ============================================================
#  Closira AI Customer Support Workflow
#  Business: Bloom Aesthetics Clinic
#  Model: Groq API - Llama 3.3 70B
# ============================================================

import json
import os
import re
from datetime import datetime
from groq import Groq

# ── Load SOP data ────────────────────────────────────────────
def load_sop():
    # Load the SOP file from the same folder as this script
    sop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sop.json")
    with open(sop_path, "r") as f:
        return json.load(f)

SOP = load_sop()
SOP_TEXT = json.dumps(SOP, indent=2)

# ── Groq client setup ─────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── System prompt ────────────────────────────────────────────
# Rules are numbered and explicit so the model follows them reliably.
# low_confidence escalation is removed — the model cannot reliably
# self-report uncertainty, so we handle it through out_of_scope instead.
SYSTEM_PROMPT = """You are a friendly customer support assistant for Bloom Aesthetics Clinic.

STRICT RULES:
1. Answer ONLY using the SOP data below. Never invent prices, services, or policies.
2. If the question is not covered in the SOP, say:
   "I don't have that information. Let me connect you with our team."
   Then add on a new line: [ESCALATE: out_of_scope]
3. If the customer sounds angry, upset, or complains, respond with empathy first, then add:
   [ESCALATE: sentiment_negative]
4. If the customer asks a medical question, respond carefully, then add:
   [ESCALATE: medical_question]
5. If the customer asks to negotiate pricing, politely decline, then add:
   [ESCALATE: pricing_negotiation]
6. Keep responses short and warm — like a real clinic receptionist.
7. Never make up information. If unsure, escalate.

SOP DATA:
""" + SOP_TEXT

# ── Lead qualification questions ─────────────────────────────
# Asked after the first FAQ answer so the flow feels natural
QUALIFICATION_QUESTIONS = [
    "Have you visited us before, or is this your first time?",
    "Which treatment interests you — Botox, Fillers, or a free consultation?",
    "Are you looking to book soon, or still researching?"
]

# ── Negative sentiment keywords and phrases ──────────────────
# Covers single words AND multi-word phrases for better detection
NEGATIVE_SENTIMENT = [
    "angry", "furious", "terrible", "awful", "ridiculous",
    "worst", "hate", "rip off", "unacceptable", "not happy",
    "disappointed", "bad service", "frustrated", "very upset",
    "disgraceful", "waste of time", "useless", "disgusting"
]

# ── Helper: Send message to AI and get reply ─────────────────
def ask_ai(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages
    )
    return response.choices[0].message.content

# ── Helper: Check for escalation tag in AI reply ─────────────
# Using [^\]]+ instead of \w+ so multi-word reasons like
# sentiment_negative and pricing_negotiation are captured correctly
def detect_escalation(text):
    match = re.search(r'\[ESCALATE:\s*([^\]]+)\]', text)
    return match.group(1).strip() if match else None

# ── Helper: Check for negative sentiment in user message ─────
def is_negative_sentiment(text):
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in NEGATIVE_SENTIMENT)

# ── Helper: Generate session summary ─────────────────────────
def generate_summary(history, lead_data, escalation_log):
    prompt = (
        "Summarise this customer support session in exactly 4 sections:\n"
        "1. Customer Intent\n"
        "2. Key Details Collected\n"
        "3. SOP Gaps Identified\n"
        "4. Recommended Next Action\n\n"
        "Conversation:\n" + json.dumps(history) +
        "\n\nLead Data:\n" + json.dumps(lead_data) +
        "\n\nEscalations:\n" + json.dumps(escalation_log)
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ── Run qualification questions ───────────────────────────────
def run_qualification(history, lead_data):
    print("\n--- Lead Qualification ---\n")
    for i, question in enumerate(QUALIFICATION_QUESTIONS):
        print("Agent: " + question + "\n")
        answer = input("You: ").strip()
        if answer.lower() == "quit":
            return False  # user wants to exit
        lead_data["q" + str(i + 1)] = {"question": question, "answer": answer}
        # Add to history so the AI has context for future replies
        history.append({"role": "assistant", "content": question})
        history.append({"role": "user", "content": answer})
    print()
    return True

# ── Main workflow ─────────────────────────────────────────────
def run_workflow():
    print("\n" + "=" * 55)
    print("  Bloom Aesthetics Clinic — AI Support (Closira)")
    print("=" * 55)
    print("Type 'quit' to end the session.\n")

    history = []         # Full conversation turns
    lead_data = {}       # Qualification answers
    escalation_log = []  # Escalation events with reason + time
    escalated = False
    qualification_done = False

    print("Agent: Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        # ── Stage 3: Sentiment check BEFORE calling AI ───────
        # Catches obvious angry messages without wasting an API call
        if is_negative_sentiment(user_input):
            reply = "I'm really sorry to hear that. Let me connect you with a human agent right away."
            print("\nAgent: " + reply + "\n")
            escalation_log.append({
                "reason": "sentiment_negative",
                "trigger": user_input,
                "time": str(datetime.now())
            })
            print("[ESCALATED — Reason: sentiment_negative]\n")
            history.append({"role": "assistant", "content": reply})
            escalated = True
            break

        # ── Stage 1: FAQ answering ────────────────────────────
        ai_reply = ask_ai(history)

        # Strip the escalation tag before showing to customer
        clean_reply = re.sub(r'\[ESCALATE:[^\]]+\]', '', ai_reply).strip()
        print("\nAgent: " + clean_reply + "\n")
        history.append({"role": "assistant", "content": clean_reply})

        # ── Stage 3: Check if AI flagged an escalation ───────
        reason = detect_escalation(ai_reply)
        if reason:
            escalation_log.append({
                "reason": reason,
                "trigger": user_input,
                "time": str(datetime.now())
            })
            print("[ESCALATED — Reason: " + reason + "]\n")
            escalated = True
            break

        # ── Stage 2: Lead qualification (once, after first reply)
        # Runs naturally after the first answered question
        if not qualification_done:
            qualification_done = True
            still_going = run_qualification(history, lead_data)
            if not still_going:
                break
            print("Agent: Thank you! Is there anything else I can help you with?\n")

    # ── Stage 4: Conversation summary ────────────────────────
    print("=" * 55)
    print("  Generating Session Summary...")
    print("=" * 55)
    summary = generate_summary(history, lead_data, escalation_log)
    print("\nSUMMARY\n")
    print(summary)

    # Save full session to file
    session = {
        "escalated": escalated,
        "lead_data": lead_data,
        "escalations": escalation_log,
        "summary": summary,
        "history": history
    }
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_log.json")
    with open(log_path, "w") as f:
        json.dump(session, f, indent=2)
    print("\n[Session saved to session_log.json]")


if __name__ == "__main__":
    run_workflow()
