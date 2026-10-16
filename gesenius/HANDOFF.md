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

Rules that matter:

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
