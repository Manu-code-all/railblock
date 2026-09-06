# Package 4 — Testing and documentation

**Owner: Member 4 · Due Friday 5 September**

Your job is to find the things that will embarrass us on stage, while there is
still time to fix them. You do not need to code — you need to use the app
badly on purpose.

---

## Deliverable A — work the checklist

`test-checklist.md` lists everything the system should do. Go through it and
mark each line PASS or FAIL. Do it on a laptop that is **not** Manu's — half of
all demo failures are things that only worked on the developer's machine.

## Deliverable B — the bug log

Every failure goes in `bug-log.md` with the steps to reproduce it. A bug report
that cannot be reproduced cannot be fixed. Three lines is enough:

```
What I did:      submitted a request with duration 9999
What happened:   the solver never returned, screen sat spinning
What I expected: a message saying no window is that long
```

**Then try to break it deliberately.** This is the valuable part:

- Submit a request longer than any window
- Set a deadline in the past, or day 99
- Duration of 0, or negative, or text
- An empty title, or a 500-character title
- Submit forty requests for the same section on the same night
- Publish a plan, then submit another request — what happens to the plan?
- Click Solve twice quickly
- Reload the page halfway through
- Resize to a phone-sized window

## Deliverable C — the user guide

`user-guide.md`. One page. Someone who has never seen RailBlock should be able
to submit a request and produce a plan by following it. Screenshots help more
than paragraphs.

Judges sometimes ask to try it themselves. This is what you hand them.

---

## What good looks like

Ten reproducible bugs is a great result, not a bad one. Every one you find on
Friday is one that does not happen in front of a judge on Sunday.
