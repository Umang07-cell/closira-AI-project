# Test: Conversation Summary

**Scenario:** Full session ending naturally with quit. Summary covers intent, details, gaps, next action.

---

**Agent:** Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?

**You:** What are your opening hours?

**Agent:** We're open Monday to Saturday, 9 AM to 7 PM. Is there anything else I can help you with?

--- Lead Qualification ---

**Agent:** Have you visited us before, or is this your first time?

**You:** I've been before

**Agent:** Which treatment interests you — Botox, Fillers, or a free consultation?

**You:** Fillers this time

**Agent:** Are you looking to book soon, or still researching?

**You:** Ready to book

**Agent:** Thank you! Is there anything else I can help you with?

**You:** What's the cancellation policy?

**Agent:** We require at least 24 hours notice if you need to cancel your appointment. Anything else?

**You:** quit

---

SUMMARY

1. Customer Intent: Returning customer checking hours and cancellation policy, ready to book Fillers.
2. Key Details Collected:
   - Returning customer
   - Interested in: Dermal Fillers
   - Booking timeline: Ready to book now
3. SOP Gaps Identified: None.
4. Recommended Next Action: Confirm Filler appointment. Send WhatsApp booking confirmation.

---
RESULT: PASS — Clean structured summary generated at session end covering all 4 required sections.
