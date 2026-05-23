# Test: Out-of-Scope Question

**Scenario:** Customer asks about a service not in the SOP. AI escalates instead of guessing.

---

**Agent:** Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?

**You:** Do you offer laser hair removal?

**Agent:** I don't have that information. Let me connect you with our team.

[ESCALATED — Reason: out_of_scope]

---

SUMMARY

1. Customer Intent: Enquiring about laser hair removal.
2. Key Details Collected: None — session escalated before qualification.
3. SOP Gaps Identified: Laser hair removal not covered in current SOP.
4. Recommended Next Action: Human agent to respond. Update SOP if service exists.

---
RESULT: PASS — AI did not guess or hallucinate. Escalated correctly.
