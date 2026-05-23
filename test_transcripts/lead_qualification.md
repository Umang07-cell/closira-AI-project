# Test: Lead Qualification

**Scenario:** AI answers first, then asks 3 qualification questions and collects lead data.

---

**Agent:** Hi! Welcome to Bloom Aesthetics Clinic. How can I help you today?

**You:** Hi, I'm interested in your services

**Agent:** We offer Botox from £200, Dermal Fillers from £250, and free initial consultations. We're open Monday to Saturday, 9 AM to 7 PM. You can book via WhatsApp or our website. What would you like to know more about?

--- Lead Qualification ---

**Agent:** Have you visited us before, or is this your first time?

**You:** First time

**Agent:** Which treatment interests you — Botox, Fillers, or a free consultation?

**You:** I'd like a free consultation first

**Agent:** Are you looking to book soon, or still researching?

**You:** I want to book this week

**Agent:** Thank you! Is there anything else I can help you with?

**You:** How do I book?

**Agent:** You can book via WhatsApp or through our website. Please note we require 24 hours notice if you need to cancel. Anything else?

**You:** quit

---

SUMMARY

1. Customer Intent: First-time visitor interested in booking a free consultation.
2. Key Details Collected:
   - New customer (first visit)
   - Interested in: Free Consultation
   - Booking timeline: This week
3. SOP Gaps Identified: None.
4. Recommended Next Action: Send booking link via WhatsApp. Confirm slot for this week.

---
RESULT: PASS — All 3 qualification questions asked after first answer. Lead data collected and summarised.
