# Package 1 — Railway domain rules

**Owner: Member 1 · Due Friday 5 September**

You are the only person on the team who will actually know how Indian Railways
plans maintenance blocks. That matters more than it sounds: the solver is only
as good as the rules we give it, and a judge who works in railways will spot a
missing rule immediately.

Two deliverables.

---

## Deliverable A — the rules worksheet

Fill in `rules-worksheet.md`. For every rule you find, record:

1. **What the rule is**, in one plain sentence.
2. **Where you found it** — circular number, manual section, page, or a URL.
3. **Whether we model it** — you will be able to tell from the list of what we
   already model, below.
4. **How it would be modelled**, in plain words. Not code. For example:
   *"a block on a double-line section may only be taken on one line at a time"*
   becomes *"treat each line as its own section"*.

**Aim for 12 to 15 rules.** Quality over volume — a rule you can cite beats
five you half-remember.

### What the solver already models

| Already in | Meaning |
|---|---|
| Section exclusivity | Only one department may hold a track section at a time |
| Traffic-free windows | Work only happens inside approved possession windows |
| Block duration | Each job has a fixed length in minutes |
| Deadlines | Each job must finish by the end of a given day |
| Crew limits | Each department can run only so many blocks at once |
| Priority | 1 routine to 5 safety-critical, used to decide what gets dropped |
| Window disruption cost | Daytime windows cost train paths; night windows do not |

Anything you find that is **not** on that list is exactly what we want.

### Where to look

- Indian Railways **Block Working Rules** and zonal engineering circulars
- **General and Subsidiary Rules (G&SR)** — the block working chapter
- Ministry of Railways **eBlock / Corridor Block** guidelines
- Recent news or CAG reports on block utilisation — good for the impact numbers
- YouTube walkthroughs by railway officers are legitimate and often clearer
  than the manuals — just note them as the source

Track your questions in `open-questions.md` as you go.

---

## Deliverable B — the honesty slide

One slide, in `honesty-slide.md`. Two columns:

**What is real** — the constraints we genuinely model and solve.
**What is simplified** — what a production system would add.

This is not a weakness. Judges have watched a hundred teams oversell a
prototype; being the team that states its own boundary is a credibility win, and
it defuses the hardest question in the room before it is asked.

Keep it to eight lines total. Plain language.

---

## How this reaches the code

Manu and the technical member read your worksheet and pick the two or three
highest-value rules to add. Your research goes straight into the solver — this
is the one non-coding package that changes what the system actually does.
