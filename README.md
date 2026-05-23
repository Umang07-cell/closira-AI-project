# Closira AI Customer Support Workflow
### Bloom Aesthetics Clinic — Assignment Submission

---

## What This Is

A Python CLI application that simulates an AI-powered customer support agent for an aesthetics clinic.
Built using the Groq API with Llama 3.3 70B. Handles FAQ answering, lead qualification,
escalation detection, and conversation summarisation in a single workflow.

---

## Setup

### 1. Install dependencies
```bash
pip install groq
```

### 2. Set your API key
```bash
export GROQ_API_KEY=your_api_key_here
```
Get a free API key at: https://console.groq.com

### 3. Run the workflow
```bash
python main.py
```

Type your message and press Enter. Type `quit` to end the session and generate a summary.

---

## Project Structure

```
closira_project/
├── main.py                    # Main workflow (all 4 stages)
├── sop.json                   # SOP data for Bloom Aesthetics Clinic
├── prompt_design.md           # System prompt + design decisions
├── README.md                  # This file
├── session_log.json           # Auto-generated after each session
└── test_transcripts/
    ├── in_scope_question.md
    ├── out_of_scope.md
    ├── escalation_trigger.md
    ├── lead_qualification.md
    └── conversation_summary.md
```

---

## How the 4 Stages Work

| Stage | How it works |
|-------|-------------|
| **FAQ Answering** | System prompt injects full SOP JSON. Model answers only from it. |
| **Lead Qualification** | 3 structured questions asked after the first answered question. Answers stored in `lead_data`. |
| **Escalation Detection** | Two layers: keyword pre-check on user input, then regex parse of `[ESCALATE: reason]` tags in AI reply. |
| **Conversation Summary** | Separate API call at session end with full conversation + lead data as context. |

---

## Conversation Flow

```
User sends first message
        ↓
AI answers from SOP
        ↓
3 qualification questions asked naturally
        ↓
Conversation continues (FAQ answering)
        ↓
User types quit  OR  escalation triggered
        ↓
Summary generated + saved to session_log.json
```

---

## Escalation Triggers

| Trigger | How detected |
|---------|-------------|
| Out-of-scope question | AI self-reports `[ESCALATE: out_of_scope]` |
| Negative sentiment | Keyword + phrase pre-check on user input |
| Medical question | AI self-reports `[ESCALATE: medical_question]` |
| Pricing negotiation | AI self-reports `[ESCALATE: pricing_negotiation]` |

---

## Trade-offs & Known Limitations

- **No persistent memory** — each session is independent (no database).
- **Keyword-based sentiment** — works for clear cases; a dedicated sentiment model would be more accurate for edge cases.
- **Single SOP file** — in production this would be a versioned database.
- **No frontend** — CLI only, as per assignment requirements.
- **Lead qualification is linear** — fixed 3 questions in a fixed order.

---

## Dependencies

- `groq` — Groq API client
- Python 3.8+
- No other external libraries required
