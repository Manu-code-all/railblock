# Package 2 — Real corridor data

**Owner: Member 2 · Due Friday 5 September**

Right now the system runs on a corridor we invented. It works, but "we made
the data up" is a weak answer to a judge. Your job is to replace it with a real
stretch of Indian Railways, built from public timetable data.

You do not need to code. You fill in three spreadsheets and Manu loads them.

---

## The three files

Open them in Excel or Google Sheets. Keep the header row exactly as it is and
save as CSV.

### `sections.csv` — the stretch of track

| column | meaning | example |
|---|---|---|
| `id` | short code, no spaces | `SEC-A` |
| `name` | the two stations it runs between | `Phulera – Jaipur` |

Pick **one real corridor of 5 to 8 sections**. A section is the track between
two adjacent stations. Any busy route works — Delhi–Mathura, Jaipur–Alwar,
Mumbai–Pune. Choose one where NTES shows plenty of trains.

### `windows.csv` — when the track can be taken

| column | meaning | example |
|---|---|---|
| `section` | must match an `id` in sections.csv | `SEC-A` |
| `days` | which days this repeats — `0-6`, or `0,2,4` | `0-6` |
| `start` | 24-hour clock | `01:00` |
| `end` | 24-hour clock | `05:00` |
| `disruption` | 0 for night, 5 for daytime | `0` |

One row covers a repeating window, so a nightly window across a week is a
single row — not seven.

**How to find real windows:** on NTES, look up a section and find the longest
stretch with no trains. On most routes that is somewhere between 00:30 and
05:00. That gap is your night window. If you find a quiet afternoon gap, add it
as a second row with disruption 5.

### `requests.csv` — the maintenance work

| column | meaning | example |
|---|---|---|
| `dept` | exactly `ENGG`, `S&T`, or `TRD` | `ENGG` |
| `section` | must match an `id` in sections.csv | `SEC-A` |
| `title` | what the work is | `Rail grinding, km 12-18` |
| `duration_min` | how long it takes | `180` |
| `priority` | 1 routine … 5 safety-critical | `4` |
| `deadline_day` | must finish by end of this day (0 = first day) | `3` |

**Aim for 18 to 24 requests** spread across the three departments.

- **ENGG** — track: rail grinding, tamping, ballast cleaning, weld renewal,
  level-crossing work, culvert repair
- **S&T** — signalling: point machine replacement, axle counter calibration,
  signal cable renewal, interlocking work, track circuit tuning
- **TRD** — overhead wires: OHE mast replacement, contact wire tension,
  insulator cleaning, feeder cable renewal, neutral section repair

Realistic durations run 90 to 240 minutes. **Make sure a few requests compete
for the same section on the same night** — that contention is what the solver
exists to resolve, and a corridor where everything fits trivially makes for a
dull demo.

---

## Do two corridors

**Corridor 1** — a comfortable one where everything fits. This is the main demo.

**Corridor 2** — deliberately overloaded: three or four urgent jobs on one
section, all due the same day, that cannot all fit. This drives the conflict
demo, which is the strongest thirty seconds we have.

Put them in `corridor-1/` and `corridor-2/`.

---

## Where to get the data

- **NTES** — enquiry.indianrail.gov.in — train timetables by station
- **erail.in** — easier to read for a whole route
- **India Rail Info** — section maps and station codes
- Any zonal railway timetable PDF

You are not looking for anything confidential. Public arrival and departure
times are enough to find the gaps.

---

## When you are done

Tell Manu. He runs one command to load your corridor, and the whole system —
every screen, the solver, the block orders — runs on your data instead of ours.

Note anything you were unsure about in `open-questions.md`. Judges ask where
data came from, and "we took it from the public NTES timetable for this
section" is a strong answer we should all be able to give.
