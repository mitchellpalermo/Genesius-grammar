# Gesenius' Hebrew Grammar — modern edition: handoff

This is a multi-session project. **Every session starts by reading this whole
file**, then runs `python3 tools/proof_status.py next` and works that chunk.
All state lives on disk in this folder; nothing depends on any earlier
conversation. Work from this folder (`gesenius/` in the
`gesenius-grammar-modernize-ac64c1` worktree). Each run commits its work
locally with `tools/proof_commit.py` (Mitch asked for this, 2026-10-16);
never push.

## What Mitch asked for (decisions already made — do not re-ask)

- A modernized PDF of *Gesenius' Hebrew Grammar*, Kautzsch–Cowley 2nd English
  edition (1910). Public domain.
- **All attribution stays exactly as on the 1910 title page** (Gesenius;
  "as edited and enlarged by the late E. Kautzsch, Professor of Theology in the
  University of Halle"; "Second English edition revised in accordance with the
  twenty-eighth German edition (1909) by A. E. Cowley"; "with a facsimile of the
  Siloam inscription by J. Euting, and a table of alphabets by M. Lidzbarski";
  Oxford at the Clarendon Press).
- **Styled like hebrew.tools**: Plus Jakarta Sans + Noto Sans Hebrew, the
  green palette and rainbow accent gradient from
  `apps/hebrew-tools/src/styles/global.css` and `Layout.astro`.
- **6×9 in trade-book page.**
- **A note near the table of contents** saying it was reformatted by an
  artificial intelligence tool, and **beside it a QR code** captioned exactly
  *"If you desire to verify against the original scan here"* linking to
  `https://ia600109.us.archive.org/26/items/geseniushebrewgr00geseuoft/geseniushebrewgr00geseuoft.pdf`.
  (Done: `tools/frontmatter.py`.)
- **Light wording modernization** — rule-based, listed in the edition note,
  reversible: `tools/modernize.py`. Applied at build time, never written into
  the proofread wikitext. Scripture references are rendered in SBL form
  (`1 Sam 15:6` for Gesenius' `1 S 15⁶`). § numbers and paragraph letters are
  never changed. *thou/thee/ye* in glosses are kept (they mark number).
- **Source text: the English Wikisource transcription**, and **every page
  Wikisource has not proofread is proofread here against the scan** (Mitch
  chose this knowing it is slow). Wikisource's paradigm pages are unproofread
  and wrong in places; paradigms are re-transcribed from the scan.
- **The three indexes** (subjects, Hebrew words, passages) are transcribed from
  the scan. Wikisource has only scraps of them.
- Mitch saw the sample (`build/sample.typ`, §22 + Paradigm B) and chose to go
  ahead; keep its look unless he asks for changes.

## Layout of this folder

| Path | What |
|---|---|
| `scan/geseniushebrewgr00geseuoft.pdf` | the scan (gitignored; also at the URL above). PDF page = printed page + 24 |
| `ws/pages.json` | Wikisource `Page:` wikitext for every scan page, with its proofread level (fetched 2026-10-16) |
| `ws/additions.json` | the *Additions and Corrections* subpages the text transcludes |
| `proof/status.tsv` | **the queue** — one row per page: chunk, status (`todo`/`done`/`flagged`/`skip`), notes |
| `proof/pages/<n>.wiki` | **working copy** of each queued page — this is what you correct |
| `proof/corrections.tsv` | every fix applied, page / old / new (written by `proof_fix.py`) |
| `proof/runs.tsv` | one timed row per run (written by `proof_lock.py release`) — `proof_status.py estimate` projects hours left from it |
| `proof/run.lock` | present while a run is working the queue |
| `proof/strips/` | scratch images (gitignored, safe to delete) |
| `tools/convert.py` | wikitext → Typst converter (templates, refs, footnotes, tables) |
| `tools/paradigms.py`, `render_paradigm.py` | verb paradigms as checked data, and their tables |
| `tools/frontmatter.py` | title page, verso, edition note + QR, contents |
| `build/gesenius.typ` | the Typst page design (tokens, margins, headings, margin letters) |
| `build/sample.typ` | the approved sample (§22 + Paradigm B) |
| `fonts/` | Plus Jakarta Sans, Noto Sans, Noto Sans Hebrew (OFL) |

Tools: system `python3` runs the proof tools. The build tools need
`mwparserfromhell` and `qrcode`, which are in `.venv/` here (gitignored; recreate
with `python3 -m venv .venv && .venv/bin/pip install mwparserfromhell qrcode
pillow`). Typst 0.15, poppler and ImageMagick are installed on this Mac.
Rebuild the sample: `.venv/bin/python -I tools/build_sample.py ws build && (cd
build && typst compile --font-path ../fonts sample.typ sample.pdf)`.

## Chunk order

`python3 tools/proof_status.py summary` shows all of them.

1. **B01–B31** — body pages (12 per chunk). Protocol A.
2. **P01–P05** — paradigm spreads. Protocol B. Paradigm B (scan 534–535) is
   already done.
3. **I01–I09** — index pages 557–622. Protocol C.
4. **S1** — build the whole book. Protocol D. Do not start S1 until
   `summary` shows everything else done.

A session takes the next chunk, finishes it, and if it has budget left, takes
the next. Stop between pages, never mid-page: a page is only `done` once its
fixes are saved. Only one run works the queue at a time: `tools/proof_lock.py`
enforces it (a lock older than 2 hours counts as abandoned — longer than any
chunk, shorter than a usage-limit reset). If you stop a run by hand, run
`python3 tools/proof_lock.py abandon` before restarting; the next run resumes
the half-done page (see the skill's "Resume safely").

### Running it on a loop

The project skill `gesenius-proofread` (`.claude/skills/gesenius-proofread/`
at the worktree root) is one run: lock, next chunk, unlock, log. Start a
session in this worktree and run it on a fixed interval:

    /loop 30m /gesenius-proofread

A self-paced `/loop /gesenius-proofread` schedules each run from the end of the
last one, so a run killed by a usage limit ends the loop; a fixed interval
keeps firing and resumes on its own after the reset. The loop stops itself
when only the build (S1) is left; the build is started by hand.

## Protocol A — proofreading a body page

For each `todo` page in the chunk:

1. `python3 tools/proof_page.py <n>` prints
   - the four scan strips to read (`proof/strips/<n>-1..4.png`, 1.4× zoom),
   - an **English diff** against the scan's OCR layer — pointers only,
   - the **Hebrew sheet** (`proof/strips/<n>-heb-*.png`): every Hebrew word on
     the scan page, enlarged ~3.6× and numbered in reading order,
   - the numbered list of Hebrew in the wikitext, then the wikitext itself.
2. Read all four strips and the Hebrew sheet(s). Compare:
   - **English**: missing or extra words, especially an English gloss after a
     Hebrew word, and OCR slips (`and` for `2nd`, `fern` for `fem.`,
     `ioc`/`I.`). Use the diff to find them, the image to decide.
   - **Hebrew**: walk the sheet against the numbered list — consonants first
     (final letters, ה/ח/ת, ב/כ, ד/ר, ו/ז/י), then vowels (tsere vs sheva vs
     segol, qamets vs patah, holem placement), shin/sin dot, dagesh, the
     stress mark ֫. The sheet catches most but not all Hebrew; anything it
     missed, check in the strips, and zoom when unsure:
     `python3 tools/proof_zoom.py <n> <strip>:<x0>,<y0>,<x1>,<y1> …`
     (coordinates in the strip image's pixels; several crops → one image).
   - **References**: Bible chapter/verse numbers and § references/letters.
   - **Italics, footnotes, paragraph letters** (`GHGmargin-letter`) present
     and in the right place.
3. Fix with `python3 tools/proof_fix.py <n> 'old' 'new' ['old' 'new' …]`.
   Each `old` must be unique on the page — include `text=…}}` or neighbouring
   words. It logs to `proof/corrections.tsv`.
4. `python3 tools/proof_status.py done <n> "<short summary of fixes>"`, or
   `flag <n> "<what you could not resolve>"` if something stays uncertain.
   Before `done`, log each close judgment call (faint print, a reading you
   chose between two, Wikisource text deliberately left alone) with
   `python3 tools/proof_review.py add <n> "<question>" "<choice>"`. Mitch
   checks `proof/review.tsv` later and sets each row's status to `ok` or `fix`;
   `proof_review.py list` shows the open ones.

Rules that matter:

- **Broken type is not a reading** (Mitch, 2026-10-16). Where the print is
  plainly damaged — a dropped or broken letter or point, a split word like
  `c curs` or `I will le` — use the word the printer intended, and log the
  case with `proof_review.py`. This covers only obvious mechanical damage;
  an author's or printer's genuine misprint (a wrong verse number, a wrong
  form) stays as printed, per the next rule.
- **The scan is the authority, not grammar.** Do not "correct" a form to what
  you expect. If print and expectation disagree and the print is legible, the
  print wins. If the print is illegible, leave Wikisource's reading and `flag`.
- **Hebrew lists keep Wikisource's convention**: in a run like
  `{{GHGheb|text=A}}, {{GHGheb|text=B}}` the items are in left-to-right
  *visual* order as printed, and the renderer isolates each item so it prints
  that way. A multi-word phrase inside one `GHGheb` is in normal logical order.
- **ʾ is alef, ʿ is ayin** in transliterations; check which one is printed.
- **Never modernize while proofreading.** The wikitext stays a faithful copy;
  modernization happens in `modernize.py` at build.
- Keep Wikisource's markup (templates, `<ref>`, `<section>` tags). Don't
  reflow or reformat lines — make the smallest exact replacement.
- Wikisource sometimes encodes a printed `ψ` as `book=Ps`: that is fine.

Pilot measurements (page 230): about 10 fixes on an unproofread page — mostly
Hebrew vowel/letter slips plus OCR `and`→`2nd`. Expect a handful per page.

## Protocol B — paradigm spreads (P01–P05)

Paradigms are rebuilt as data in `tools/paradigms.py` (see `PARADIGM_B` and
its docstring for the cell format: forms in printed left-to-right order, `*`
marks a model form, `—` empty, `~text` for English like `~wanting.`,
`|4` rowspan). For each spread:

1. Start from the Wikisource wikitext in `proof/pages/<n>.wiki` as a draft,
   but expect wrong letters and shifted cells (its rows often have extra empty
   cells).
2. Render the scan at 300 dpi and read it in horizontal strips at ~1.6× zoom;
   zoom single cells with `proof_zoom.py` (after `proof_page.py <n>` has made
   the strips) whenever a vowel is uncertain.
3. Write the paradigm as a new `PARADIGM_<X>` entry. A, C and Q have different
   shapes from B (pronoun suffix tables, verbs with suffixes) — extend
   `render_paradigm.py` for them rather than forcing B's shape.
4. List every departure from Wikisource in the entry's docstring, as B does.
5. Mark the spread's pages done.

## Protocol C — the indexes (I01–I09)

Scan pages 557–622: Index of Subjects, Index of Hebrew Words, Index of
Passages, each in two columns. Wikisource has raw OCR for a few pages (with
`{{hebrew missing}}`) and nothing for most.

Transcribe each scan page into `proof/pages/<n>.wiki` (create it if missing),
reading the page column by column, in the same wikitext conventions as the
body so the converter handles it:

- one entry per line; sub-entries continue the line as printed (`Article, 35:
  syntax of, 126: with demonstrative force, 126 ''a'', ''b'': …`);
- section letters in italics `''a''`, `N.` for "note";
- Hebrew in `{{GHGheb|text=…}}` — in the Hebrew-word index, the headword;
- Index of Passages: a line per verse, `Gn 1 2 . . . 141 c` style is fine —
  keep the book headings as `== Genesis ==` lines and the verse/section pairs
  as `2 | 141 ''c''`.
- start the page with `<!-- scan <n>, printed <n-24>, <which index> -->`.

These references are to **sections**, so they stay valid in the new layout.

## Protocol D — the build (S1)

Not yet written; `build/sample.typ` + `tools/build_sample.py` are the
pattern. What S1 must do:

- `tools/build_book.py`: assemble scan pages 25–531 in order from
  `proof/pages/<n>.wiki` where it exists, else `ws/pages.json`; convert with
  `convert.py`; insert paradigms (`paradigms.py`) and indexes; write
  `build/book.typ`; compile with `typst compile --font-path fonts`.
- **Structure**: Parts and Chapters are free-form centred blocks in the
  wikitext (see the Contents, scan pages 15–20). Map them to `=` / `==`
  headings by § number (Introduction before §1; First Part + Ch. I at §5;
  Ch. II at §18; Second Part at §30; Ch. I The Pronoun §32; Ch. II The Verb
  §38; Ch. III The Noun §79; Ch. IV The Particles §99; Third Part Syntax at
  §106; Ch. II The Sentence §140; and the sub-heads inside chapters), and
  drop the original blocks.
- Front matter: Translator's Preface, From the German Preface, List of
  Abbreviations (add a line that Scripture references now follow SBL style),
  the Siloam inscription (scan pages 22–23: keep the facsimile as an image
  cropped from the scan) and the Table of Early Semitic Alphabets (locate it
  in the scan; image). *Additions and Corrections* are already applied inline
  by Wikisource (`GHGcorrected`); say so in the edition note rather than
  reprinting the list.
- Edition note (`frontmatter.py`): update "Sources" with the real numbers —
  pages proofread here, number of corrections (`wc -l proof/corrections.tsv`),
  and that paradigms and indexes were transcribed from the scan.
- Known converter gaps to handle: a footnote inside a § heading (render it,
  keep it out of the outline/bookmarks); `{{raw image}}`; `colbegin/colend`
  (two-column index); `GHGhebT` blocks; tables in §§93/95 (noun paradigms,
  inline in the body); converter `warnings` — print and clear them all.
- QA: read every warning; spot-check ~20 pages across the book as images
  against the scan; check the outline/bookmarks; check that § cross-reference
  links resolve.
- Deliver the PDF to Mitch (SendUserFile) and say plainly what was and was not
  verified.

## Log

Append one line per run: the summary `proof_lock.py release` prints (start →
end, minutes, chunks, pages, fixes, min/page), then anything the next run must
know. The numbers come from `proof/runs.tsv`; don't type them by hand.

- 2026-10-16 — set up the pipeline, sample approved, page 230 proofread as the
  pilot (10 fixes), Paradigm B verified. Next: B01.
- 2026-10-16 — B01: 2026-10-16T14:06:52 → 15:21:53, 75.0 min, 11 pages (1 flagged),
  40 fixes, 6.8 min/page (page 33 was done by an earlier run of this session
  that was interrupted and recorded `abandoned`; the 75 min includes a
  usage-limit pause, so the true pace is faster). Flagged 66: the Babylonian
  vowel-mark footnote is placeholders and the print has two signs the wiki
  omits; it needs images cropped from scan 67 at build time. Recurring in this
  stretch: wrong Hebrew letter in a word (ד/ר, ח/ה, ג/נ, final ם for medial מ),
  missing or extra punctuation around ed. Mant./Baer variant readings, and
  English OCR slips (fortz, peps, hems, fall for full). Next: B02.
- 2026-10-16 — B02: 2026-10-16T15:41:04 → 15:47:29, 6.4 min, 12 pages (0 flagged),
  43 fixes, 0.5 min/page. The B01 figure includes a usage-limit pause, so the
  two runs bracket the real pace; trust `estimate` only after a few more rows.
  This stretch (§§ 27–30) has the same Hebrew-letter slips as B01 (ד/ר twice:
  בִּֽיהוּדָה again, חרק, ספרד; ה/ח: חָיָה, וֶֽחְיֵה) plus split § letters
  written as `{{GHGpar|72|d}}d` — grep for `}}[a-z]\b` after a GHGpar on later
  pages. The print's ס and ם are indistinguishable in unpointed roots; keep
  Wikisource's reading there. Next: B03.
- 2026-10-16 — B03: 2026-10-16T16:11:06 → 16:15:42, 4.6 min, 12 pages (0 flagged),
  21 fixes, 0.4 min/page. §§ 30–39 (pronouns, article, start of the verb) is
  cleaner than §§ 20–29: three pages had no fixes. Patterns here: transliterated
  alef typed as ’ instead of ʾ (seven on page 130 alone — grep `''’` per page),
  a book name misattached to a verse ref (`on Lev {{…book=Dt…}}`), and stray
  dagesh in paradigm forms (הָקְּטַל). Page 131's חִיא for הוּא is a genuine
  misprint in the 1910 text; kept as printed. Next: B04.
- 2026-10-16 — B04: 2026-10-16T16:41:07 → 16:46:10, 5.0 min, 12 pages (0 flagged),
  24 fixes, 0.4 min/page. §§ 40–48 (flexion of Perfect, Infinitive, Imperative,
  Imperfect). Most fixes are stray or wrong points in paradigm forms
  (יִקְטִֹל, תִָּקְטֹ֫לְנָה, לְבַשֹׁ, חֳָרָ֑בִי — grep for two vowels on one letter),
  one wrong consonant per page or so (לָמַר, שְׂמַה), and a garbled pair of
  Hebrew words with the semicolon inside one GHGheb (page 150). Pages 145, 147,
  153 needed nothing. Next: B05.
- 2026-10-16 — B05 partial (usage limit): pages 154–160 done, 161–165 still todo.
  Fixes: OCR `and`→`2nd` twice (pages 155, 156 — grep `the and`), doubled
  vowels, Ex/Ez book mix-up. The run row above in runs.tsv covers only these
  seven pages. Next: finish B05 from page 161.
- 2026-10-16 — B05 finished: pages 161–165 done, 0 flagged, 10 fixes. OCR word
  slips (emission→omission, gone→tone, "put out on"), Greek ξ→χ in μάχεσθαι,
  vowel slips (Piʿ̄l→Piʿēl, Puʿal ŏ→ă), נְלְחַם→נִלְחַם. Next: B06.
- 2026-10-16 — B06 done: pages 166–176, 180; 0 flagged, 36 fixes. Look-alike
  letters (ט/מ in יַקְטִיל etc. on 172, ט/מ in מְלוֹשְׁנִי 175, ה/ח in חסר 169, ג/נ
  in הִתְגַּדֵּל 174), stray/doubled points (וָאֲצַוֶּה, הִתְגֹּעֲשׁוּ, זֹרְמוּ), ’→ʾ,
  mojibake "aŒ¬"→ā̆ (180 fn), wrong book in a ref (Is→Jb 13:27, p.174), one
  section end tag par54→par55 (176). Next: B07.
- 2026-10-16 — B07 done: pages 181–185, 194–196, 200–204; 0 flagged, 28 fixes.
  ר/ו (וַיְבָרֶךְ 194), dropped/stray points (קְטָלַתְהָ 184, מְשַׁלֵּחֲךָ,
  וַתֵּעָצַר, וַיָּסָב), missing final ם (וְישַׁעֲכֶם 196), English slips
  (more→mere, from→form, soon→seen, yă→hă-sēb), book=Job→Jb template refs (204),
  a Stade § wrongly linked as GHGpar (200, unlinked). Next: B08.
- 2026-10-16 — B08 done: pages 205–207, 209–217; 0 flagged, 40 fixes. Look-alikes
  (ו/ז תֵּזְלִי 210, ר/ו יִירַשׁ 212, ת/ה הָבָה 214, ה/ח וַיּוֹכַח 215), stray/missing
  points (ׄ upper dot → holem, יְבֹשׁ/יְבֹשֶׁת on 213, 216), reversed RTL pairs
  "X ;Y" (207, 211), English OCR (east→cast, arrears→appears, soon-style slips),
  a Ju-for-Is ref with stray "is" (205). Unresolved but left (print faint):
  2 S 14 verse on p.217 (wiki 19, print looks like 13). Next: B09.
- 2026-10-16 — B09 done: pages 218–229; 0 flagged, 52 fixes. Heavy ד/ר and ג/נ
  confusion in §72–73 (תְּרוֹמֵם גּוֹי, וַיֵּרֹמּוּ, הֵרֹמּוּ, מוּר, רִיב יָרִיב, הרים,
  בֹּרַאֲךָ), ב/כ in suffix כֶם (196-style, again 229), missing dagesh in וַיָּ forms
  (224, 226, 228), OCR English (mast/mase/muse→masc, band→hand, censonantal),
  two Stade § refs mislinked as GHGpar (219), extra Est 4:14 ref not in print
  removed (224), duplicate section-begin tag removed (226). Next: B10.
- 2026-10-16 — Added the review log (`tools/proof_review.py`, `proof/review.tsv`)
  for close judgment calls, at Mitch's request; backfilled 6 calls from B07–B10.
  `proof_fix.py` now refuses no-op fixes and escapes line breaks/tabs when
  logging, and four rows of corrections.tsv that a multi-line fix had split
  across lines (pages 99, 108, 202, 235) were rejoined. B05–B09 were never
  committed at the time (the per-run commit step was missed); committed now in
  one catch-up commit, with B10 pages 231–235 included as work in progress.
- 2026-10-16 — B10 done: pages 231–241 (§74 l–§76 d); 0 flagged. Lock timer
  spans the review-log interruption, so its minutes overstate the run. Fixes:
  ד/ר and נ/ו slips (כָּרֹת, רְאוֹת, נַאֲוָה, הֶחְבְּאַתָה), §-letter margin markers
  on 241 moved to the print's positions (76 b at "2.", c at (b), d at (c)),
  Stade/Barth § refs unlinked (234), ’/‛→ʾ/ʿ. 5 review items logged (236, 237,
  239, 240, plus backfill). Open policy question in review.tsv: broken type
  ('c curs' p.234 kept vs 'I will le' p.239 left as 'be'). Next: B11.
- 2026-10-16 — Broken-type rule added (see Protocol A): obvious mechanical
  damage → intended word + review log. Applied to p.234 ('c curs'→'occurs').
- 2026-10-16 — B11 done: pages 242–244, 259–267 (§76 e–§78, §84b o–§87 p); 0 flagged,
  52 fixes, 5.2 min. Same look-alike pattern (ח/ת תְּהִלִּים, ג/נ אִגְּרוֹת, ח/ת
  חָזוֹן, ז/ו מִזְבֵּחַ, ח/ה חָכְמוֹת), English OCR (heating→healing, musc→masc,
  ground-from), ‛/’→ʿ/ʾ throughout, a broken {{GHGcite|title|…}} template (262),
  Barth/Stade § refs unlinked (264). 4 review items (242, 243 ×2, 266). The new
  no-op guard in proof_fix.py fired once and wrote nothing, as intended. Next: B12.
- 2026-10-16 — B12 done: pages 268–279 (§87 p–§91 e); 0 flagged, 38 fixes, 4.8 min.
  Look-alikes (ה/ח חֲלוֹם, ם/ס כִּסֵּא, פ/מ הַמֶּלֶךְ, נ/כ suffix table כֶם, ח/ת
  בְּתוֹכְכֶם), garbled pointing (נַהֲרַיִם, גְּנֻבְתִי … לָיְלָה, דַּיֶּךָּ, the
  suffix table on 278), musc→masc again, ‛/’→ʿ/ʾ. 2 review items (272, 275).
  Next: B13.
- 2026-10-17 — B13 done: pages 280–285, 288–289, 301–304 (§91 e–§95 q). The first
  run stalled overnight after page 282 and was recorded `abandoned`; the resume
  run did 283–304 (3.8 min). 0 flagged, 48 fixes total. Paradigm tables (288–289,
  301–302) carry many one-letter slips (ד/ר צְדָקָה, ה/ח חֶרְפָּה חֻקּוֹת, ט/מ זִמָּה,
  נ/ג גְּבִרְתְּכֶם, ס/ם מַלְכַּת) and an "eorum" for "earum" in the 283 table.
  0 review items. Several queued loop firings arrived while the run was stalled;
  they were folded into this one run. Next: B14.
- 2026-10-17 — B14 done: pages 306–308, 311–315, 317–320 (§96–§100 o, end of the
  numerals and start of the particles). 0 flagged, 32 fixes. Recurring issue: Wikisource sometimes stored
  two-word Hebrew in visual left-to-right order (עָשָׂר<ref> עַשְׁתֵּי on 314,
  רִבּוֹא שְׁתֵּי on 315); restored logical order and logged both. Also letter
  swaps אָמתַ֫יִם→מָאתַ֫יִם, אָו→אָז, מִוֶּה→מִזֶּה, and non-Gesenius § refs (Barth,
  Stade) unlinked. Review items: 311 (§97 holem policy), 314 ×2 (row order; Ex
  45¹² misprint for Ez kept), 315. Next: B15.
- 2026-10-17 — B15 done: pages 321–332 (§100 o–§105 b, end of the particles).
  0 flagged. The visual-order problem from B14 recurred in fused spans: אֱלַי
  (אֲלַי) on 328 and the Gn 7:13 / 1 K 21:10 run on 331 (rebuilt). Also ב/כ
  swaps in כָּכֶם (327), ט/מ and dagesh slips in the מִן table (מִמְּךָ, מִמֵּךְ),
  ה/ח (בֵּינֵיהֶם, אֲלֵהֶן, וָפָח), and Wikisource had silently corrected the
  printed "2 K 22³⁰" to 1 K (330) — restored as printed. Review items: 321, 325,
  328, 330, 331. Eight queued loop firings arrived during the run and were folded
  into it. Next: B16.
- 2026-10-17 — B16 done: pages 333–346 (§106–§109 f, start of Syntax: the
  perfect, imperfect, cohortative and jussive). 0 flagged, 35 fixes. Mostly
  ד/ר (יִסָּפֵר, אֲשֶׁר twice on 343, וְהַנַּעַר), ב/כ and ב/נ (כַּאֲשֶׁר 335,
  יַנְחֵנִי 339, הָטְבָּעוּ 338), פ/מ (שָׁמָּה 346), wrong book names in refs (Gn→Is
  63, Ps→Is 40), a dropped 1 K 7:8, a mislabelled "(b)" for "(a)" on 345, and
  many unitalicized cross-reference letters. Review item: 342 (Ez 12:12 word
  order). Next: B17.
- 2026-10-17 — B17 done: pages 347–355, 357–359 (§109 g–§112 dd: jussive,
  imperative, imperfect and perfect with wāw consecutive). 0 flagged, 46 fixes.
  Hebrew: ה/ח (יְחַיּוּ, וַתִּירְאִי, וְהֶחֱרַשְׁתִּי, וְהָיוּ), ת/ה (ויהי ×2), נ/ג
  (וְגָדַעְתִּי), נ/ו (וִיכַזֵּב), stray dagesh (מֵאָז). Wrong § numbers in
  cross-refs (§ 144 r→114 r, § 112 c→111 c), a missing "(" on 359, and many
  unitalicized section letters. Visual-order spans again on 349 and 352. Review
  items: 347 (Jb 37:22 vs 27:22), 349, 350 (Dn 15¹⁹ misprint kept), 352.
  Next: B18.
