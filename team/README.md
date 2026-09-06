# Team plan — 3 to 6 September

**Internal hackathon: 7 September.** On the day, our technical member does the
development and the finishing. Everything in this folder is what the rest of us
produce beforehand so that he starts with a working system, real data and a
clear list of what to do — instead of spending the morning working out what the
project even is.

Five people, four days, four packages. Each has its own folder with the files
to fill in.

| Who | Package | Folder |
|---|---|---|
| Manu | Run the build, test it, brief the technical member | — |
| Member 1 | Railway domain rules | `1-domain/` |
| Member 2 | Real corridor data | `2-data/` |
| Member 3 | Demo and pitch | `3-pitch/` |
| Member 4 | Testing and documentation | `4-test/` |

---

## What we are building

**RailBlock.** Three railway maintenance departments — Engineering, Signalling
and Traction — each book track possession independently, so blocks clash and
maintenance windows are wasted. RailBlock takes all three departments' requests
plus the timetable and returns one conflict-free schedule that the solver
*proves* is optimal. When the requests genuinely cannot all fit, it names the
exact set that is in conflict.

Since the MVP it has gained a database, four role-based views (the three
departments plus a controller), an explanation for every scheduled block, and
exportable block orders.

**The one line everyone should be able to say:** *the solver does not predict a
good schedule, it proves one — and when no schedule exists it tells you exactly
which requests are fighting.*

---

## Day by day

### Wednesday 3 September — tonight
- **Everyone:** read this file and your own package's README.
- **Everyone:** re-watch our MVP video so we are all describing the same thing.
- **Manu:** get the system running locally and confirm it works.
- **Member 2:** start collecting timetable data — this has the longest lead time.

### Thursday 4 September
- **Manu:** test the role views and the explanation panel; report anything broken.
- **Member 1:** work through the rules worksheet.
- **Member 2:** fill in `sections.csv` and `windows.csv` for corridor 1.
- **Member 3:** draft the five-minute demo script.
- **Member 4:** run the test checklist against what exists and start the bug log.

### Friday 5 September
- **Manu:** load Member 2's real corridor and check the solver handles it.
- **Member 1:** finish the worksheet; write the "what is real, what is simplified" slide.
- **Member 2:** finish corridor 2; confirm both load without errors.
- **Member 3:** slides finished; judge Q&A list written.
- **Member 4:** finish the bug log; start the user guide.

### Saturday 6 September
- **Manu:** freeze the code, write the handover note, rehearse the demo.
- **Member 4:** finish the user guide.
- **Everyone:** full dress rehearsal of the five-minute demo, twice.
- **Evening:** brief the technical member — walk him through the handover note
  and the open list so he begins on Sunday already knowing what to do.

### Sunday 7 September — hackathon
Technical member develops and polishes. Manu supports and answers questions
about the system. Member 3 presents. Members 1, 2 and 4 handle judge questions
in their own areas.

---

## Ground rules

- **Do not edit code** unless you are Manu or the technical member. Everything
  else is filled in through the files in your folder.
- **If something is unclear, write the question down** in your package's README
  rather than guessing. An honest open question is more useful on the day than a
  confident wrong answer.
- **Nothing gets claimed that is not built.** Member 1's honesty slide exists
  precisely so we can say plainly what is real. Judges trust teams that scope
  honestly, and they always find the gap anyway.
