import re, glob, io, os, markdown

SP = os.path.dirname(os.path.abspath(__file__))
parts = sorted(glob.glob(os.path.join(SP, "part[0-9][0-9].md")))
raw = "\n\n".join(io.open(p, encoding="utf-8").read().strip() for p in parts)

# medals encode nothing typography can't; strip them
raw = raw.replace("🥇 ", "").replace("🥈 ", "").replace("🥉 ", "").replace("🏆 ", "")

md = markdown.Markdown(extensions=["tables", "toc", "sane_lists", "attr_list", "fenced_code"],
                       extension_configs={"toc": {"permalink": False}})
body = md.convert(raw)

# collapse the double <hr> section breaks into one rule
body = re.sub(r"(<hr\s*/?>\s*){2,}", '<hr class="brk" />', body)
# wrap tables for horizontal scroll
body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
# split the "Organisation / Score" run-on paragraph into a strapline + a verdict plate
body = re.sub(
    r"<p>(<strong>Organisation:</strong>.*?)\n<strong>(Score: .*?)</strong></p>",
    r'<p class="meta">\1</p>\n<p class="verdict"><span>\2</span></p>',
    body, flags=re.S)

SHORT = {
    "65": "PS 65 · Train Induction", "70": "PS 70 · NEP Timetable",
    "33": "PS 33 · Internship Allocation", "64": "PS 64 · Document Overload",
    "125": "PS 125 · DPR Risk", "54": "PS 54 · Rainwater Harvesting",
    "26": "PS 26 · NAMASTE / ICD-11", "121": "PS 121 · R&amp;D Proposals",
    "22": "PS 22 · Rail Throughput",
}
nav = []
for t in md.toc_tokens:
    if t["level"] != 1:
        continue
    name = re.sub(r"^(①|②|③|④|⑤|⑥|⑦|⑧)\s*", "", t["name"])
    m = re.match(r"PS (\d+)", name)
    if m:
        label = SHORT[m.group(1)]
    elif name.startswith("SIH 2025"):
        label = "Executive Summary"
    elif "CROSS-STATEMENT" in name:
        label = "Comparison Table"
    elif "FINAL RECOMMENDATION" in name:
        label = "Final Recommendation"
    elif "FULL-FIELD SCREEN" in name:
        label = "All 105, Screened"
    elif "SIH 2026" in name:
        label = "SIH 2026 · Software List"
    elif "REVISED VERDICT" in name:
        label = "Revised Verdict"
    else:
        label = name
    nav.append((t["id"], label))
navhtml = "\n".join(
    f'<a href="#{i}"><span class="n">{k:02d}</span><span class="t">{lbl}</span></a>'
    for k, (i, lbl) in enumerate(nav, start=1))

CSS = """
:root{
  --paper:#EEF1F0; --surface:#FFFFFF; --ink:#12181C; --muted:#55635E;
  --rule:#D2DAD7; --rule-soft:#E2E8E5; --accent:#1F7A5A; --accent-soft:#DCEBE4;
  --amber:#8A6100; --critical:#A62B1F; --code:#F3F6F4;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#0D1311; --surface:#141C19; --ink:#E4EAE7; --muted:#8FA09A;
    --rule:#233029; --rule-soft:#1B2521; --accent:#4FBF8F; --accent-soft:#173026;
    --amber:#D9A32B; --critical:#E0685A; --code:#111917;
  }
}
:root[data-theme="dark"]{
  --paper:#0D1311; --surface:#141C19; --ink:#E4EAE7; --muted:#8FA09A;
  --rule:#233029; --rule-soft:#1B2521; --accent:#4FBF8F; --accent-soft:#173026;
  --amber:#D9A32B; --critical:#E0685A; --code:#111917;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto} *{animation:none!important;transition:none!important}}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
  font-size:17px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
.shell{display:grid; grid-template-columns:266px minmax(0,1fr); gap:0; max-width:1240px; margin:0 auto}

/* ---- rail ---- */
.rail{
  position:sticky; top:0; align-self:start; height:100dvh; overflow-y:auto;
  padding:34px 22px 40px 26px; border-right:1px solid var(--rule);
}
.brandmark{
  font-family:"JetBrains Mono",ui-monospace,monospace; font-size:10px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--accent); margin:0 0 6px;
}
.brandname{
  font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
  font-weight:700; font-size:20px; line-height:1.12; letter-spacing:-.018em; margin:0 0 4px;
}
.brandsub{font-size:12.5px; color:var(--muted); margin:0 0 22px; line-height:1.45}
.rail nav{display:flex; flex-direction:column; gap:1px; border-top:1px solid var(--rule-soft); padding-top:12px}
.rail nav a{
  display:grid; grid-template-columns:26px 1fr; gap:8px; align-items:baseline;
  padding:6px 8px 6px 0; text-decoration:none; color:var(--muted); border-radius:3px;
}
.rail nav a .n{font-family:"JetBrains Mono",monospace; font-size:10px; color:var(--accent); opacity:.75}
.rail nav a .t{font-size:13px; line-height:1.35; font-family:"Bricolage Grotesque",Arial,sans-serif; font-weight:500}
.rail nav a:hover{color:var(--ink)}
.rail nav a:focus-visible{outline:2px solid var(--accent); outline-offset:2px}

/* ---- article ---- */
main{padding:52px 46px 120px; min-width:0}
.doc{max-width:70ch}
h1,h2,h3{font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; text-wrap:balance}
h1{
  font-size:clamp(28px,3.4vw,40px); line-height:1.06; letter-spacing:-.028em; font-weight:800;
  margin:0 0 14px; padding-top:8px;
}
.doc > h1:not(:first-child){
  margin-top:76px; padding-top:26px; border-top:2px solid var(--ink);
}
h2{
  font-size:21px; letter-spacing:-.012em; font-weight:700; margin:44px 0 12px;
  padding-bottom:7px; border-bottom:1px solid var(--rule);
}
h3{font-size:17px; font-weight:700; letter-spacing:-.005em; margin:32px 0 8px; color:var(--accent)}
p{margin:0 0 15px}
strong{font-weight:700}
em{font-style:italic}
a{color:var(--accent); text-underline-offset:2px}
ul,ol{margin:0 0 16px; padding-left:22px}
li{margin-bottom:7px}
li::marker{color:var(--muted)}
hr.brk{border:0; height:0; margin:0}

.meta{
  font-family:"JetBrains Mono",monospace; font-size:11.5px; letter-spacing:.01em;
  color:var(--muted); margin:-6px 0 16px; line-height:1.6;
}
.meta strong{font-weight:400}
.verdict{
  display:flex; margin:0 0 26px; padding:12px 16px;
  background:var(--accent-soft); border-left:3px solid var(--accent); border-radius:0 3px 3px 0;
}
.verdict span{
  font-family:"JetBrains Mono",monospace; font-size:12.5px; font-weight:700;
  letter-spacing:.005em; color:var(--ink); line-height:1.5;
}

/* ---- tables ---- */
.tw{
  overflow-x:auto; margin:0 0 26px; border:1px solid var(--rule);
  border-radius:4px; background:var(--surface); max-width:min(100%,1040px);
}
table{border-collapse:collapse; width:100%; font-size:13.5px; line-height:1.5}
thead th{
  font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.09em;
  text-transform:uppercase; font-weight:500; color:var(--muted);
  text-align:left; padding:11px 14px; border-bottom:1px solid var(--rule);
  background:var(--code); white-space:nowrap; vertical-align:bottom;
}
tbody td{
  padding:11px 14px; border-bottom:1px solid var(--rule-soft);
  vertical-align:top; font-variant-numeric:tabular-nums;
}
tbody tr:last-child td{border-bottom:0}
tbody tr:nth-child(even){background:color-mix(in srgb, var(--code) 55%, transparent)}
td strong{font-weight:700}
td:first-child{white-space:nowrap}
table td:first-child:has(+ td){white-space:normal}

/* ---- code / diagrams ---- */
pre{
  overflow-x:auto; background:var(--code); border:1px solid var(--rule);
  border-radius:4px; padding:16px 18px; margin:0 0 26px; max-width:min(100%,1040px);
}
code{font-family:"JetBrains Mono",ui-monospace,monospace; font-size:12px}
pre code{font-size:11.5px; line-height:1.55; white-space:pre}
p code,li code,td code{
  background:var(--code); border:1px solid var(--rule-soft);
  padding:1px 5px; border-radius:3px; font-size:12.5px;
}
blockquote{margin:0 0 20px; padding-left:16px; border-left:2px solid var(--rule); color:var(--muted)}
::selection{background:var(--accent); color:var(--surface)}

@media (max-width:920px){
  .shell{grid-template-columns:1fr}
  .rail{position:static; height:auto; border-right:0; border-bottom:1px solid var(--rule); padding:26px 22px 20px}
  .rail nav{display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:2px 14px}
  main{padding:32px 22px 90px}
  body{font-size:16px}
  .doc > h1:not(:first-child){margin-top:52px}
}
"""

HTML = f"""<title>SIH Shortlist Dossier</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600&family=JetBrains+Mono:wght@400;500;700&display=swap">
<style>{CSS}</style>
<div class="shell">
  <aside class="rail">
    <p class="brandmark">Smart India Hackathon</p>
    <p class="brandname">Shortlist Dossier</p>
    <p class="brandsub">Independent evaluation of eight shortlisted problem statements &mdash; ranked, scored, and argued.</p>
    <nav aria-label="Sections">
{navhtml}
    </nav>
  </aside>
  <main>
    <article class="doc">
{body}
    </article>
  </main>
</div>
"""

out = os.path.join(SP, "sih_dossier.html")
io.open(out, "w", encoding="utf-8").write(HTML)
print("wrote", out, len(HTML), "bytes;", len(nav), "nav items")
for i, l in nav: print(" -", l[:70])
