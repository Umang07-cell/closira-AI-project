# Prompt Design — Closira AI Workflow
## Bloom Aesthetics Clinic

---

## 1. Full System Prompt

```
You are a friendly customer support assistant for Bloom Aesthetics Clinic.

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
{ ...full SOP JSON injected at runtime... }
```

---

## 2. Design Decisions & Reasoning

### Why inject SOP as JSON?
JSON is structured and unambiguous. It makes it easy for the model to reference exact values
(prices, hours, channels) without paraphrasing incorrectly. Plain text SOPs are more prone
to misinterpretation.

### Why use explicit escalation tags?
Tags like `[ESCALATE: out_of_scope]` are machine-readable. The Python code parses them
with regex — escalation detection does not rely on fuzzy string matching. It is
deterministic and easy to extend.

### Why use numbered rules?
LLMs follow explicit numbered rules more consistently than prose instructions. Each rule
maps to one failure mode (hallucination, wrong escalation, wrong tone).

### Why ask qualification questions after the first answer?
Asking questions before the user gets any help feels like interrogation. Real clinic
receptionists answer first, then gather details. This makes the flow feel natural.

---

## 3. Hallucination Prevention

- System prompt says **"Answer ONLY using the SOP data below"** — explicit, not implied.
- Full SOP is injected into every request so the model always has the source of truth.
- When info is missing, the model is told to say a specific scripted phrase rather than improvise.
- Out-of-scope questions immediately trigger escalation — the model is not allowed to guess.

---

## 4. Escalation Logic

Escalation is handled in two layers:

**Layer 1 — Code-side (before AI call):**
- A list of negative keywords and phrases is checked against the user's message.
- If matched, the session escalates immediately without calling the API.
- This catches obvious cases (angry, frustrated, not happy, bad service, etc.) reliably.

**Layer 2 — Model-side (after AI reply):**
- The system prompt instructs the model to append `[ESCALATE: reason]` for specific triggers.
- Python regex `r'\[ESCALATE:\s*([^\]]+)\]'` parses the tag from the reply.
- The tag is stripped from the customer-facing message before display.
- `[^\]]+` is used instead of `\w+` to correctly capture multi-word reasons like `sentiment_negative`.

This dual-layer approach means even if the model fails to self-report, the code catches it.

**Note on low_confidence:** Self-reported uncertainty (`[ESCALATE: low_confidence]`) was
removed. LLMs cannot reliably self-assess confidence in this context — out_of_scope covers
the same failure mode more reliably.

---

## 5. Tone and Persona

- Persona: warm, professional clinic receptionist
- Concise responses (max_tokens=500) — not chatty
- Empathetic language required before escalating negative sentiment
- Avoids clinical jargon — accessible to general public
- Redirects gracefully rather than saying "I cannot"

---

## 6. Four-Stage Flow

| Stage | Implementation |
|-------|---------------|
| FAQ Answering | Model answers from SOP via system prompt |
| Lead Qualification | 3 fixed questions asked after first FAQ answer |
| Escalation Detection | Keyword pre-check + regex tag parsing |
| Conversation Summary | Separate API call with full conversation as context |
