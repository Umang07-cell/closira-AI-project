# Test: In-Scope Question

**Scenario:** Customer asks about Botox prices. AI answers from SOP only, then qualifies.

---

**Agent:** Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?

**You:** What are your Botox prices?

**Agent:** Our Botox treatments start from £200. I'd recommend booking a free consultation first so our team can give you an accurate quote based on your needs!

--- Lead Qualification ---

**Agent:** Have you visited us before, or is this your first time?

**You:** First time

**Agent:** Which treatment interests you — Botox, Fillers, or a free consultation?

**You:** Botox

**Agent:** Are you looking to book soon, or still researching?

**You:** Looking to book soon

**Agent:** Thank you! Is there anything else I can help you with?

**You:** No that's all

**You:** quit

---

SUMMARY

1. Customer Intent: Enquiring about Botox pricing with intent to book soon.
2. Key Details Collected: First-time visitor, interested in Botox, ready to book.
3. SOP Gaps Identified: None — all questions answered from SOP.
4. Recommended Next Action: Book a free consultation for an accurate price quote.

---
RESULT: PASS — AI answered from SOP only. No hallucination. Qualification completed after first answer.
