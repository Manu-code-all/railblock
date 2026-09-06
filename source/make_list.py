#!/usr/bin/env python3
"""Generate the software-only SIH 2026 problem statement index (Markdown + HTML)."""
import json, os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(BASE, "source", "sih2026.tsv")

# Data-quality notes carried over from the handoff (section 7).
DISPUTED_HW = {87, 88, 96, 109}   # tagged Hardware, read as pure software
OUT_OF_SCOPE = {114: "CAD modelling in Autodesk Forma, not a software build",
                116: "CAD modelling in Autodesk Revit, not a software build"}

rows = []
for line in open(TSV, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line:
        continue
    num, org, title, cat = line.split("|")
    rows.append({"num": int(num), "org": org, "title": title, "cat": cat})

software = [r for r in rows if r["cat"] == "Software"]
disputed = [r for r in rows if r["num"] in DISPUTED_HW]
hardware_n = len(rows) - len(software)

# organisations ordered by descending count, ties broken by first appearance
first_seen, counts = [], {}
for r in software:
    counts[r["org"]] = counts.get(r["org"], 0) + 1
    if r["org"] not in first_seen:
        first_seen.append(r["org"])
order = sorted(first_seen, key=lambda o: (-counts[o], first_seen.index(o)))

for r in software:
    r["flag"] = OUT_OF_SCOPE.get(r["num"], "")

# ---------------------------------------------------------------- markdown
md = ["# SIH 2026 - Software Problem Statements",
      "",
      "**%d of 192** statements. The %d tagged Hardware are excluded." % (len(software), hardware_n),
      "IDs run `SIH26001`-`SIH26192`; the number below is the last three digits.",
      "",
      "## By organisation",
      "",
      "| Organisation | Count |",
      "|---|---|"]
for o in order:
    md.append("| %s | %d |" % (o, counts[o]))
md += ["", "---", ""]

for o in order:
    md += ["## %s (%d)" % (o, counts[o]), ""]
    for r in [x for x in software if x["org"] == o]:
        note = "  **[out of scope: %s]**" % r["flag"] if r["flag"] else ""
        md.append("- **%d** - %s%s" % (r["num"], r["title"], note))
    md.append("")

md += ["---", "",
       "## Disputed labels",
       "",
       "Tagged **Hardware** in the source but reading as pure software. Verify on the SIH portal",
       "before excluding - if the portal agrees they are software, they belong in the list above.",
       ""]
for r in disputed:
    md.append("- **%d** - %s - %s" % (r["num"], r["org"], r["title"]))
md += ["",
       "Reverse error: **114** and **116** are tagged Software but are Autodesk CAD modelling",
       "exercises. They are listed above under their organisation and marked, but are out of",
       "scope regardless of label.",
       ""]

with open(os.path.join(BASE, "SIH2026_Software_PS.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# ---------------------------------------------------------------- html
payload = json.dumps({"software": software, "disputed": disputed,
                      "order": order, "counts": counts}, ensure_ascii=False)

sections = []
for o in order:
    items = []
    for r in [x for x in software if x["org"] == o]:
        flag = ('<span class="flag" title="%s">out of scope</span>' % html.escape(r["flag"])) if r["flag"] else ""
        items.append(
            '<li class="row"><span class="num">%03d</span>'
            '<span class="title">%s%s</span></li>' % (r["num"], html.escape(r["title"]), flag))
    sections.append(
        '<section class="org" data-org="%s"><h2><span class="org-name">%s</span>'
        '<span class="org-count">%d</span></h2><ul class="rows">%s</ul></section>'
        % (html.escape(o), html.escape(o), counts[o], "".join(items)))

disputed_items = "".join(
    '<li class="row"><span class="num">%03d</span><span class="title">%s'
    '<span class="org-tag">%s</span></span></li>'
    % (r["num"], html.escape(r["title"]), html.escape(r["org"])) for r in disputed)

chips = "".join(
    '<button class="chip" data-filter="%s" aria-pressed="false">%s'
    '<span class="chip-n">%d</span></button>' % (html.escape(o), html.escape(o), counts[o])
    for o in order)

TEMPLATE = """<title>SIH 2026 Software Docket</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {
  --ground:#F3F4F1; --surface:#FBFBF9; --ink:#151A19; --muted:#5C6A66;
  --rule:#DCDED8; --accent:#0D5A52; --accent-soft:#0D5A5214; --flag:#8A5A00;
  --flag-soft:#8A5A0014; --shadow:0 1px 2px #151A190A;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:#121615; --surface:#181D1C; --ink:#E8EBE7; --muted:#94A19C;
    --rule:#2A322F; --accent:#5FC9BB; --accent-soft:#5FC9BB1A; --flag:#D6A439;
    --flag-soft:#D6A4391A; --shadow:0 1px 2px #00000040;
  }
}
:root[data-theme="dark"] {
  --ground:#121615; --surface:#181D1C; --ink:#E8EBE7; --muted:#94A19C;
  --rule:#2A322F; --accent:#5FC9BB; --accent-soft:#5FC9BB1A; --flag:#D6A439;
  --flag-soft:#D6A4391A; --shadow:0 1px 2px #00000040;
}
* { box-sizing:border-box; }
body {
  background:var(--ground); color:var(--ink);
  font-family:Archivo,-apple-system,"Segoe UI",sans-serif;
  margin:0; padding:0 20px 80px; -webkit-font-smoothing:antialiased;
}
.wrap { max-width:900px; margin:0 auto; }

header.masthead { padding:56px 0 28px; border-bottom:2px solid var(--ink); }
.eyebrow {
  font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
  color:var(--accent); margin:0 0 14px;
}
h1 {
  font-family:Newsreader,Georgia,serif; font-weight:400; font-size:clamp(34px,5.5vw,52px);
  line-height:1.05; margin:0 0 16px; text-wrap:balance; letter-spacing:-.01em;
}
.standfirst { font-size:15px; line-height:1.6; color:var(--muted); max-width:62ch; margin:0; }
.standfirst strong { color:var(--ink); font-weight:600; }

.stats { display:flex; flex-wrap:wrap; gap:0; margin:28px 0 0; border-top:1px solid var(--rule); }
.stat { flex:1 1 120px; padding:14px 18px 12px; border-right:1px solid var(--rule); }
.stat:last-child { border-right:0; }
.stat b {
  display:block; font-family:"JetBrains Mono",monospace; font-size:24px; font-weight:600;
  font-variant-numeric:tabular-nums; line-height:1;
}
.stat span {
  display:block; font-size:10px; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); margin-top:7px;
}

.controls {
  position:sticky; top:0; z-index:20; background:var(--ground);
  padding:14px 0 12px; border-bottom:1px solid var(--rule); margin-bottom:8px;
}
.searchbar { display:flex; align-items:center; gap:10px; }
#q {
  flex:1; font:inherit; font-size:15px; color:var(--ink); background:var(--surface);
  border:1px solid var(--rule); border-radius:2px; padding:10px 13px; box-shadow:var(--shadow);
}
#q::placeholder { color:var(--muted); }
#q:focus { outline:2px solid var(--accent); outline-offset:1px; border-color:transparent; }
#count {
  font-family:"JetBrains Mono",monospace; font-size:12px; font-variant-numeric:tabular-nums;
  color:var(--muted); white-space:nowrap;
}
.chips { display:flex; gap:6px; overflow-x:auto; padding:11px 1px 2px; scrollbar-width:thin; }
.chip {
  font:inherit; font-size:12px; font-weight:500; white-space:nowrap; cursor:pointer;
  color:var(--muted); background:transparent; border:1px solid var(--rule);
  border-radius:2px; padding:5px 9px; display:inline-flex; align-items:center; gap:6px;
}
.chip:hover { color:var(--ink); border-color:var(--muted); }
.chip:focus-visible { outline:2px solid var(--accent); outline-offset:1px; }
.chip[aria-pressed="true"] {
  color:var(--accent); border-color:var(--accent); background:var(--accent-soft);
}
.chip-n { font-family:"JetBrains Mono",monospace; font-size:10px; font-variant-numeric:tabular-nums; opacity:.7; }

section.org { padding-top:26px; }
section.org h2 {
  display:flex; align-items:baseline; gap:12px; margin:0 0 2px;
  font-size:12px; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
  padding-bottom:7px; border-bottom:1px solid var(--ink);
}
.org-name { flex:1; }
.org-count {
  font-family:"JetBrains Mono",monospace; font-size:12px; letter-spacing:0;
  color:var(--muted); font-variant-numeric:tabular-nums;
}
ul.rows { list-style:none; margin:0; padding:0; }
li.row {
  display:flex; gap:16px; align-items:baseline;
  padding:9px 4px; border-bottom:1px solid var(--rule);
}
li.row:hover { background:var(--accent-soft); }
.num {
  font-family:"JetBrains Mono",monospace; font-size:12px; font-weight:600;
  font-variant-numeric:tabular-nums; color:var(--accent); width:34px; flex:none;
}
.title { font-family:Newsreader,Georgia,serif; font-size:17px; line-height:1.38; text-wrap:pretty; }
.flag, .org-tag {
  display:inline-block; margin-left:9px; vertical-align:1px;
  font-family:Archivo,sans-serif; font-size:10px; font-weight:600;
  letter-spacing:.07em; text-transform:uppercase; padding:2px 6px; border-radius:2px;
}
.flag { color:var(--flag); background:var(--flag-soft); border:1px solid var(--flag); }
.org-tag { color:var(--muted); background:transparent; border:1px solid var(--rule); }

.note {
  margin-top:44px; padding:20px 22px; background:var(--surface);
  border:1px solid var(--rule); border-left:3px solid var(--flag); border-radius:2px;
}
.note h3 {
  margin:0 0 8px; font-size:12px; font-weight:600; letter-spacing:.1em;
  text-transform:uppercase; color:var(--flag);
}
.note p { margin:0 0 14px; font-size:14px; line-height:1.6; color:var(--muted); max-width:62ch; }
.note ul.rows li.row:last-child { border-bottom:0; }
.note .num { color:var(--flag); }
.note .tail { margin:14px 0 0; }
.empty { padding:48px 4px; color:var(--muted); font-size:15px; display:none; }
footer {
  margin-top:48px; padding-top:18px; border-top:1px solid var(--rule);
  font-size:12px; color:var(--muted); display:flex; justify-content:space-between; gap:14px; flex-wrap:wrap;
}
@media (max-width:560px) {
  .title { font-size:16px; }
  .stat { flex-basis:50%; border-bottom:1px solid var(--rule); }
}
</style>

<div class="wrap">
<header class="masthead">
  <p class="eyebrow">Smart India Hackathon 2026 &middot; Docket</p>
  <h1>Every software problem statement, sorted by who is asking</h1>
  <p class="standfirst">All <strong>__NSOFT__ software statements</strong> of the 192 published. The __NHARD__ tagged Hardware are excluded. Full IDs run <strong>SIH26001</strong>&ndash;<strong>SIH26192</strong>; the number shown is the last three digits. The source Theme column is misaligned and has been dropped &mdash; do not trust it.</p>
  <div class="stats">
    <div class="stat"><b>__NSOFT__</b><span>Software</span></div>
    <div class="stat"><b>__NHARD__</b><span>Hardware, cut</span></div>
    <div class="stat"><b>__NORG__</b><span>Organisations</span></div>
    <div class="stat"><b>__NTOP2__</b><span>MoES + NTRO</span></div>
  </div>
</header>

<div class="controls">
  <div class="searchbar">
    <input id="q" type="search" placeholder="Search titles, organisations, or a statement number" aria-label="Search problem statements">
    <span id="count">__NSOFT__ shown</span>
  </div>
  <div class="chips" role="group" aria-label="Filter by organisation">
    <button class="chip" data-filter="" aria-pressed="true">All<span class="chip-n">__NSOFT__</span></button>
    __CHIPS__
  </div>
</div>

<main id="list">__SECTIONS__</main>
<p class="empty" id="empty">No statement matches that search.</p>

<div class="note">
  <h3>Disputed labels &mdash; check before you rely on this</h3>
  <p>These four are tagged <strong>Hardware</strong> in the source but read as pure software, so they sit outside the list above. Verify them on the SIH portal; if the portal agrees, they are fair game.</p>
  <ul class="rows">__DISPUTED__</ul>
  <p class="tail">The reverse error also exists: <strong>114</strong> and <strong>116</strong> are tagged Software but are Autodesk CAD modelling exercises. They appear above, marked, and are out of scope regardless of label.</p>
</div>

<footer>
  <span>Source: SIH 2026 published statements &middot; 500-team cap per statement</span>
  <span>Submission deadline 20 September 2026</span>
</footer>
</div>

<script>
(function () {
  var q = document.getElementById('q'),
      count = document.getElementById('count'),
      empty = document.getElementById('empty'),
      chips = Array.prototype.slice.call(document.querySelectorAll('.chip')),
      sections = Array.prototype.slice.call(document.querySelectorAll('section.org')),
      org = '';

  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    sections.forEach(function (sec) {
      var secOrg = sec.getAttribute('data-org'), visible = 0;
      Array.prototype.forEach.call(sec.querySelectorAll('li.row'), function (row) {
        var hay = (row.textContent + ' ' + secOrg).toLowerCase();
        var ok = (!org || org === secOrg) && (!term || hay.indexOf(term) !== -1);
        row.style.display = ok ? '' : 'none';
        if (ok) { visible++; }
      });
      sec.style.display = visible ? '' : 'none';
      sec.querySelector('.org-count').textContent = visible;
      shown += visible;
    });
    count.textContent = shown + ' shown';
    empty.style.display = shown ? 'none' : 'block';
  }

  q.addEventListener('input', apply);
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      org = (org === chip.getAttribute('data-filter')) ? '' : chip.getAttribute('data-filter');
      chips.forEach(function (c) {
        c.setAttribute('aria-pressed', c.getAttribute('data-filter') === org ? 'true' : 'false');
      });
      if (!org) { chips[0].setAttribute('aria-pressed', 'true'); }
      apply();
    });
  });
  window.SIH2026 = __PAYLOAD__;
}());
</script>
"""

out = (TEMPLATE
       .replace("__NSOFT__", str(len(software)))
       .replace("__NHARD__", str(hardware_n))
       .replace("__NORG__", str(len(order)))
       .replace("__NTOP2__", str(counts[order[0]] + counts[order[1]]))
       .replace("__CHIPS__", chips)
       .replace("__SECTIONS__", "".join(sections))
       .replace("__DISPUTED__", disputed_items)
       .replace("__PAYLOAD__", payload))

with open(os.path.join(BASE, "sih2026_software_list.html"), "w", encoding="utf-8") as f:
    f.write(out)

print("software=%d hardware=%d orgs=%d" % (len(software), hardware_n, len(order)))
