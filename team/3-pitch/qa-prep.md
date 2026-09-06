# Judge Q&A preparation

Write your own answer under each. Rehearse the starred ones out loud — those
are the ones that decide close calls.

Rule for all of them: **if we have not built it, say so.** "Not yet — that is
phase two" is a good answer. A bluff that gets caught costs the round.

---

## ★ How is this different from any scheduling app?

*Ours:* a scheduling app gives you **an** answer. CP-SAT proves it is **the
best** answer under the stated rules — and when no answer exists it names the
exact requests in conflict.

**Your version:**

---

## ★ Where is the AI?

Careful — this is a trap and an opportunity. We use **no machine learning at
all**, deliberately. Constraint programming is an established branch of AI
(operations research), and unlike a trained model it produces a proof rather
than a prediction. There is no accuracy figure to defend and no training data
to collect.

**Your version:**

---

## ★ Where did your data come from?

Public NTES timetables for a real corridor; Member 2 identified the traffic-free
windows from published train timings. The maintenance requests are realistic
examples, since actual departmental demands are internal to the railways.

**Your version:**

---

## ★ What happens when it says no solution?

Demo it. It names the conflicting requests and gives the arithmetic — *"these
three need 270 minutes of a 240-minute window; defer any one."* That is the
part a planner can actually act on.

**Your version:**

---

## Does it scale to the whole network?

---

## How would Indian Railways actually deploy this?

---

## How long did the solver take, and does it grow badly with size?

---

## What if a block overruns on the day?

---

## Who enters the requests in real life?

---

## What is the hardest constraint you had to model?

---

## What did you get wrong and fix?

*A good honest answer earns more than a polished non-answer. We have a real
one: the solver's built-in conflict report returned every request rather than
the minimal set, so we added a filter that removes them one at a time to find
the irreducible core.*

**Your version:**

---

## What would you build next with three more months?

---

## Questions we could not answer

Write them here as they come up in rehearsal, and bring them to Manu.

-
-
