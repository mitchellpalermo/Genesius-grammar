"""Front matter shared by the sample and the full build: title page, verso,
the edition note (AI disclaimer + QR code), and the contents."""
import qrcode
import qrcode.image.svg

from modernize import rule_descriptions

SCAN_URL = "https://ia600109.us.archive.org/26/items/geseniushebrewgr00geseuoft/geseniushebrewgr00geseuoft.pdf"


def write_qr(path: str) -> None:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=10)
    qr.add_data(SCAN_URL)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage, fill_color="#14532D")
    img.save(path)


def title_page() -> str:
    # Wording and order exactly as the 1910 title page; only the type is new.
    return r'''
#page(margin: 0pt, header: none, footer: none, numbering: none)[
  #block(width: 100%, height: 6pt, fill: accent-gradient)
  #block(width: 100%, height: 3.35in, fill: primary, inset: (x: 0.75in, top: 0.9in))[
    #set text(font: sans, fill: white)
    #text(size: 15pt, weight: "bold", tracking: 0.12em, fill: accent-light)[GESENIUS’]
    #v(0.06in)
    #text(size: 34pt, weight: "extrabold", tracking: -0.01em)[Hebrew\ Grammar]
  ]
  #block(width: 100%, inset: (x: 0.75in, top: 0.45in))[
    #set text(font: sans, fill: ink)
    #set par(justify: false, leading: 0.5em)
    #text(size: 8.5pt, tracking: 0.08em, fill: muted)[AS EDITED AND ENLARGED BY THE LATE]
    #v(0.04in)
    #text(size: 15pt, weight: "bold", fill: primary)[E. Kautzsch]
    #v(0.0in)
    #text(size: 7.5pt, tracking: 0.06em, fill: muted)[PROFESSOR OF THEOLOGY IN THE UNIVERSITY OF HALLE]
    #v(0.28in)
    #text(size: 9.5pt, weight: "bold", tracking: 0.08em)[SECOND ENGLISH EDITION]
    #v(0.04in)
    #text(size: 8.5pt, tracking: 0.06em, fill: muted)[REVISED IN ACCORDANCE WITH THE TWENTY-EIGHTH\ GERMAN EDITION (1909) BY]
    #v(0.04in)
    #text(size: 15pt, weight: "bold", fill: primary)[A. E. Cowley]
    #v(0.28in)
    #text(size: 7.5pt, tracking: 0.06em, fill: muted)[WITH A FACSIMILE OF THE SILOAM INSCRIPTION BY J. EUTING,\ AND A TABLE OF ALPHABETS BY M. LIDZBARSKI]
  ]
  #place(bottom + left, dx: 0.75in, dy: -0.7in)[
    #set text(font: sans)
    #block(width: 0.9in, height: 2pt, fill: accent)
    #v(0.06in)
    #text(size: 9pt, weight: "bold", tracking: 0.1em, fill: ink)[OXFORD]\
    #text(size: 8pt, tracking: 0.08em, fill: muted)[AT THE CLARENDON PRESS]
  ]
  #place(bottom + right, dx: -0.6in, dy: -0.55in,
    text(font: hebrew-font, size: 64pt, fill: rule, [א]))
]
'''


def verso() -> str:
    return r'''
#page(header: none, footer: none)[
  #set text(font: sans, size: 7.5pt, fill: muted)
  #set par(justify: false)
  #v(1fr)
  #align(center)[
    SECOND ENGLISH EDITION 1910 \
    #v(2pt)
    Reprinted lithographically in Great Britain at the University Press, Oxford,\
    1946, 1949, 1952, 1956, from corrected sheets of the second edition
    #v(4pt)
    #text(size: 6.5pt)[(the imprint of the copy scanned by the Internet Archive)]
  ]
  #v(0.4in)
]
'''


def edition_note(qr_path: str, sample: bool = False) -> str:
    rules = ", ".join(rule_descriptions())
    return rf'''
#page(header: none)[
  #set par(justify: false)
  #v(0.15in)
  #block(width: 100%, height: 3pt, fill: accent-gradient)
  #v(0.12in)
  #text(font: sans, size: 15pt, weight: "extrabold", fill: primary)[About this edition]
  #v(0.08in)
  #block(width: 100%, fill: bg, radius: 5pt, stroke: 0.8pt + rule, inset: 10pt)[
    #text(weight: "bold", fill: ink)[This edition has been reformatted by an artificial intelligence tool.]
    The text, the Hebrew, and the tables were re-set by software rather than by a human editor, so errors are possible. Where anything matters, check it against the original printing.
  ]
  #v(0.06in)
  #grid(columns: (1fr, 1.15in), column-gutter: 14pt,
    [
      #set text(size: 8.4pt)
      *What is the same.* The words of Gesenius, Kautzsch and Cowley, including every section number (§) and paragraph letter (_a_, _b_, _c_…), which stand in the outer margin as they did in 1910, so citations like §22#emph[c] still find their place.

      *What changed.* Modern type and layout. Scripture references are given in the modern form (#bref("1 Sam 15:6") for _1 S 15⁶_; #bref("Ps 52:5") for _ψ 52⁵_). A few old spellings are updated: {rules}. Glosses such as _ye have killed_ keep their _thou_ and _ye_, since those mark singular and plural.

      *Checking a page.* The small grey numbers in the inner margin (#text(fill: muted, size: 7pt)[p.#h(1pt)76]) mark where each page of the 1910 printing began.

      *Sources.* The running text comes from the volunteer transcription of this edition on English Wikisource. The paradigms were checked against the scan form by form, because Wikisource's paradigm pages are unproofread and contain errors. Notes added by Wikisource's editors are left out.
    ],
    [
      #align(center)[
        #box(stroke: 0.8pt + rule, radius: 5pt, inset: 7pt, image("{qr_path}", width: 100%))
        #v(4pt)
        #text(size: 7.5pt, weight: "bold", fill: primary)[If you desire to verify against the original scan here]
      ]
    ],
  )
  #v(1fr)
  #text(size: 6.5pt, fill: muted)[Original scan: archive.org/details/geseniushebrewgr00geseuoft. Public domain.]
]
'''


def contents() -> str:
    return r'''
#page(header: none)[
  #text(font: sans, size: 15pt, weight: "extrabold", fill: primary)[Contents]
  #v(0.15in)
  #show outline.entry.where(level: 1): it => { v(6pt); strong(text(fill: primary, it)) }
  #outline(title: none, depth: 3, indent: 1em)
]
'''
