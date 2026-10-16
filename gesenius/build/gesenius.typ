// Gesenius' Hebrew Grammar — modern edition, styled after hebrew.tools.
// Design tokens are copied from apps/hebrew-tools/src/styles/global.css.

#let primary = rgb("#15803D")
#let primary-light = rgb("#16A34A")
#let accent = rgb("#F59E0B")
#let accent-light = rgb("#FCD34D")
#let coral = rgb("#F43F5E")
#let grape = rgb("#7C3AED")
#let jade = rgb("#059669")
#let bg = rgb("#F0FDF4")
#let ink = rgb("#14532D")
#let muted = rgb("#6B7280")
#let hebrew-ink = rgb("#15803D")
#let rule = rgb("#BBF7D0")

// hebrew.tools' rainbow accent line, as a Typst gradient
#let accent-gradient = gradient.linear(primary, grape, coral, accent, jade)

#let sans = ("Plus Jakarta Sans", "Noto Sans")
#let hebrew-font = "Noto Sans Hebrew"

// ── Inline helpers used by the converted text ─────────────────────────────
// Hebrew is wrapped in Unicode isolates (RLI … PDI), the equivalent of the
// app's per-span dir="rtl": a list like "A, B, C" keeps its reading order.
#let he(body) = text(font: hebrew-font, fill: hebrew-ink, size: 1.14em,
  [#"\u{2067}"#body#"\u{2069}"])
#let heblock(body) = block(width: 100%, spacing: 0.9em,
  align(right, text(font: hebrew-font, fill: hebrew-ink, size: 1.14em, lang: "he", dir: rtl, body)))
#let greek(body) = text(font: ("Noto Sans",), body)
#let arabic(body) = text(font: ("Noto Sans Arabic", "Noto Sans"), body)
#let syriac(body) = text(font: ("Noto Sans Syriac", "Noto Sans"), body)
#let sc(body) = text(size: 0.82em, tracking: 0.04em, upper(body))
#let bref(s) = box(text(fill: ink, s))
#let missing() = text(fill: coral, weight: "bold", [\[Hebrew missing\]])

// A § cross-reference: a link when the target exists in this volume.
#let xref(target, body) = context {
  if query(target).len() > 0 { link(target, text(fill: primary, body)) } else { body }
}

// Margin-note machinery: place something in the outer (or inner) margin at
// the current line, whichever side that is on this page.
#let page-w = 6in
#let m-inside = 0.75in
#let m-outside = 0.9in
#let in-margin(side: "outside", dy: 0pt, width: 0.62in, body) = context {
  let pos = here().position()
  let recto = calc.odd(here().page())
  let right-side = if side == "outside" { recto } else { not recto }
  let x = if right-side {
    page-w - (if recto { m-outside } else { m-inside }) + 0.14in
  } else {
    (if recto { m-inside } else { m-outside }) - 0.14in - width
  }
  box(width: 0pt, place(top + left, dx: x - pos.x, dy: dy,
    box(width: width, align(if right-side { left } else { right }, body))))
}

// Paragraph letter (§22 a, b, c …) in the outer margin, as Gesenius prints it.
#let ml(letter) = in-margin(dy: -0.62em,
  box(fill: bg, stroke: 0.6pt + rule, radius: 3pt, inset: (x: 3.5pt, y: 2pt),
    text(font: sans, size: 7.5pt, weight: "bold", fill: primary, style: "italic", letter)))

// Where a page of the 1910 printing began — for checking against the scan.
#let origpage(n) = in-margin(side: "inside", dy: -0.5em, width: 0.5in,
  text(font: sans, size: 6pt, fill: muted, [p.#h(1pt)#n]))

// ── Headings ──────────────────────────────────────────────────────────────
#let sec(num, title, note: []) = {
  heading(level: 3, [§#h(0.25em)#num. #title])
  if note != [] { place(hide(note)) }
}

#let gtable(..args) = {
  set text(size: 8.5pt)
  set par(justify: false)
  block(width: 100%, align(center, table(
    stroke: (x, y) => (bottom: 0.4pt + rule),
    inset: (x: 4pt, y: 3.2pt),
    align: horizon,
    ..args)))
}

#let book(body) = {
  set document(title: "Gesenius' Hebrew Grammar", author: ("Wilhelm Gesenius", "Emil Kautzsch", "A. E. Cowley"))
  set page(
    width: page-w, height: 9in,
    margin: (inside: m-inside, outside: m-outside, top: 0.85in, bottom: 0.8in),
    header: context {
      counter(footnote).update(0)
      let p = here().page()
      let sel = heading.where(level: 3).or(heading.where(level: 2))
      let secs = query(sel.before(here()))
      let on-page = query(sel).filter(h => h.location().page() == p)
      if on-page.len() > 0 { secs = secs + on-page.slice(0, 1) }
      if secs.len() == 0 { return }
      if query(heading.where(level: 1)).any(h => h.location().page() == p) { return }
      set text(font: sans, size: 7.5pt, fill: muted)
      let s = secs.last()
      if calc.odd(p) {
        align(right, [#s.body])
      } else {
        align(left, [Gesenius’ Hebrew Grammar])
      }
      v(-4pt)
      line(length: 100%, stroke: 0.5pt + rule)
    },
    footer: context {
      let p = here().page()
      set text(font: sans, size: 8pt, weight: "bold", fill: primary)
      align(if calc.odd(p) { right } else { left }, counter(page).display())
    },
  )
  set text(font: sans, size: 9.4pt, fill: ink, lang: "en", region: "gb", hyphenate: true)
  set par(justify: true, leading: 0.62em, spacing: 0.85em, first-line-indent: 0pt)
  set footnote.entry(separator: line(length: 25%, stroke: 0.5pt + rule), gap: 0.45em, indent: 0pt)
  show footnote.entry: set text(size: 7.8pt)
  show footnote.entry: set par(leading: 0.5em)
  show emph: set text(style: "italic")

  show heading.where(level: 1): it => {
    pagebreak(weak: true, to: "odd")
    v(1.2in)
    block(width: 100%, height: 3pt, fill: accent-gradient)
    v(0.25in)
    set par(justify: false)
    text(font: sans, size: 22pt, weight: "extrabold", fill: primary, tracking: -0.01em, hyphenate: false, it.body)
    v(0.35in)
  }
  show heading.where(level: 2): it => {
    v(0.25in)
    block(width: 100%, inset: (x: 0pt, y: 6pt), below: 0.2in, {
      set par(justify: false)
      text(font: sans, size: 13pt, weight: "extrabold", fill: primary, hyphenate: false, it.body)
      v(-2pt)
      block(width: 1.2in, height: 2pt, fill: accent)
    })
  }
  show heading.where(level: 3): it => {
    block(above: 1.5em, below: 1.0em, breakable: false, width: 100%,
      fill: bg, radius: 4pt, inset: (x: 8pt, y: 7pt), stroke: (left: 3pt + primary),
      text(font: sans, size: 11pt, weight: "bold", fill: primary, it.body))
  }
  body
}

// ── Paradigms ─────────────────────────────────────────────────────────────
#let pform(f, star) = box({
  text(font: hebrew-font, fill: hebrew-ink, size: 1.22em, [#"\u{2067}"#f#"\u{2069}"])
  if star { text(fill: accent, weight: "bold", size: 0.9em, baseline: -0.3em, [\*]) }
})
#let parhead(id, title) = heading(level: 2, [Paradigm #id. #title])
#let ptable(caption, ncols, header, cells) = {
  set text(size: 7.6pt)
  set par(justify: false)
  block(width: 100%, breakable: false, {
    text(font: sans, size: 7.5pt, weight: "bold", fill: muted, tracking: 0.05em, upper(caption))
    v(2pt)
    table(
      columns: (auto, 1fr) + (auto,) * ncols,
      gutter: 0pt,
      stroke: none,
      inset: (x: 3pt, y: 2.6pt),
      align: (x, y) => if x < 2 { left + horizon } else { right + horizon },
      fill: (x, y) => if y > 0 and calc.even(y) { bg } else { none },
      table.header(..header),
      table.hline(stroke: 0.6pt + primary),
      ..cells,
    )
  })
}
