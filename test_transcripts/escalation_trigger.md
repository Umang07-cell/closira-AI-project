# Test: Escalation Trigger (Negative Sentiment)

**Scenario:** Customer expresses frustration. Code detects sentiment and escalates before AI call.

---

**Agent:** Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?

**You:** This is absolutely ridiculous, I've been waiting 3 days for a callback!

**Agent:** I'm really sorry to hear that. Let me connect you with a human agent right away.

[ESCALATED — Reason: sentiment_negative]

---

SUMMARY

1. Customer Intent: Complaint about a missed/delayed callback.
2. Key Details Collected: None — escalated immediately due to negative sentiment.
3. SOP Gaps Identified: No callback SLA defined in current SOP.
4. Recommended Next Action: Human agent to follow up urgently and apologise.

---
RESULT: PASS — "ridiculous" matched sentiment keyword list. Escalated with empathy before AI call.
