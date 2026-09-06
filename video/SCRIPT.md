# RailBlock — spoken script

Team Anomaly · SIH 2026 · PS SIH2026027
Total ≈ **2:58**. Word counts are set for a clear, unhurried pace (~145 wpm).

Two kinds of beat:

- **CAMERA** — you are on screen, talking to the lens.
- **VOICEOVER** — your voice over one of the supplied screen clips. Timecodes
  in `[ ]` are cues into that clip.

---

# PRESENTER A — camera only

## Beat 1 · to camera · 0:24

> Indian Railways has three departments that need the track closed to do their
> work — Engineering, Signalling, and Traction.
>
> Each one books its own blocks. Independently. Nobody sees the others' plans.
>
> So two departments book the same section on the same night. One gets
> cancelled that morning — after the crew has already travelled out.
>
> The work doesn't happen, and the trains are delayed anyway.

*Pause after "Independently." Slow down on the last line — it's the point.*

## Beat 2 · to camera · 0:14

> This isn't a prediction problem. It's a coordination problem.
>
> One team per section. Work only inside the traffic-free window — one to five
> in the morning. Limited crews. Every job has a deadline.
>
> Today, this is done by hand.

*Clip the middle list short and even, like reading out constraints.*

---

# PRESENTER B — the developer

## Beat 3 · to camera · 0:18

> We built RailBlock — one planner that takes all three departments' requests
> plus the timetable, and returns a single schedule.
>
> It runs on Google OR-Tools CP-SAT, a constraint solver. It trains no model,
> and it uses no historical data.
>
> It doesn't predict a good schedule. It proves one.

*Full stop before the last two sentences. Land them separately.*

## Beat 4 · VOICEOVER over `b04_screen.mp4` · 0:34

> `[0:00]` This is one week on the Jaipur–Gurgaon corridor. Eighteen
> maintenance requests, across six sections.
>
> `[0:09]` Colour is the department. The pale bands are the traffic-free
> windows — and every single block sits inside one.
>
> `[0:18]` Proven optimal. Solved in well under a second.
>
> `[0:24]` And zero rule violations — that's a separate checker re-testing the
> finished plan from scratch.
>
> `[0:30]` This isn't a prediction with a confidence score. The solver has
> proved that no better plan exists.

*Do not say a number for the solve time. The figure on screen changes on every
re-solve, and "well under a second" is true every time.*

## Beat 5 · VOICEOVER over `b05_screen.mp4` · 0:27

> `[0:00]` Here's what a controller actually argues about — how hard to push.
>
> `[0:06]` Slide left: protect train service. The work spreads across seven
> days, using no daytime windows at all.
>
> `[0:16]` Slide right: clear the urgent work. The same eighteen jobs, in two
> days — but now it's spending six daytime windows, and that costs train paths.
>
> `[0:26]` Both plans are optimal. The slider doesn't bend the rules. It sets
> the priority.

*Say "slide left" and "slide right" as the drag starts, not after.*

---

# PRESENTER C

## Beat 6 · VOICEOVER over `b06_screen.mp4` · 0:34

> `[0:00]` Sometimes the requests genuinely don't fit. This is the part we're
> proudest of.
>
> `[0:07]` Three emergency jobs. All on Phulera–Jaipur. All the same night.
>
> `[0:13]` It doesn't say "no solution". It names them. Ninety minutes each —
> two hundred and seventy in total. The window is two hundred and forty.
>
> `[0:22]` Any two of them fit. All three can't. So there's no single request
> to blame — and it worked that out.
>
> `[0:30]` A planner can act on this. Nobody can act on "no solution found."

*This is the strongest 30 seconds in the video. Leave a full beat of silence
before the last line.*

## Beat 7 · to camera · 0:17

> It works the same for one division or for all sixty-eight — with no change to
> the code.
>
> It feeds the eBlock system the railways already use, so there's nothing new
> for field staff to learn. The whole stack is open source, so there's no
> licensing cost.
>
> And better-planned maintenance means safer track — for thirteen million
> passengers a day.

## Beat 8 · to camera · 0:10

> What you just watched is real — the solver, the plans, all of it.
>
> What's next is connecting it to the live railway systems.
>
> Team Anomaly, Galgotias University.

*Sign off looking at the lens. Don't rush it and don't smile it away.*

---

# Running order

| Beat | Who | Type | Length | Runs to |
|---|---|---|---|---|
| 1 | A | camera | 0:24 | 0:24 |
| 2 | A | camera | 0:14 | 0:38 |
| 3 | B | camera | 0:18 | 0:56 |
| 4 | B | voiceover | 0:34 | 1:30 |
| 5 | B | voiceover | 0:27 | 1:57 |
| 6 | C | voiceover | 0:34 | 2:31 |
| 7 | C | camera | 0:17 | 2:48 |
| 8 | C | camera | 0:10 | **2:58** |

If you run over three minutes, cut beat 7 down to the first and last sentence.
That is the cheapest twelve seconds in the script.

---

# Delivery notes

- **Read it out loud five or six times before recording.** The goal is to stop
  needing the page — not to reproduce it exactly. Wording that drifts is fine;
  wording that is word-perfect sounds recited.
- **Pause at the paragraph breaks.** They are written as breathing points, and
  they are what stops it sounding rushed.
- **If you fluff a line and recover naturally, keep the take.** It reads as a
  person talking, which is the whole point.
- **Never say a number the screen contradicts.** The only figures spoken are
  18 requests, 6 sections, 7 days, 2 days, 6 windows, 90 / 270 / 240 minutes,
  68 divisions and 13 million passengers — all of which are stable.
- For voiceover, watch the clip once through before recording against it.
