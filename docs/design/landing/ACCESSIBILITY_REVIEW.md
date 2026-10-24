# Static mobile/readability assessment

Revision landing-ux0-r1; scope is rendered artwork, not WCAG certification or responsive application testing.
Primary 390px mobile pages have 24px gutters, 342px content, 40/45 hero headings and 17/26 body text.
48px primary CTA is a designed target only; navigation text target/focus behavior needs later implementation.
No hovering, interaction, safe-area behavior, scroll tracking or browser chrome exists in these artboards.

| Solid foreground / background | Computed sRGB contrast |
|---|---:|
| #172D32 / #F5F2EA | 12.88:1 |
| #4C6264 / #F5F2EA | 5.80:1 |
| #FFFFFF / #21675F | 6.62:1 |
| #21675F / #F5F2EA | 5.92:1 |
| #FFFFFF / #172D32 | 14.40:1 |

Mobile UX computed these values; the Chief rechecks them in verification. Reference threshold is
[W3C minimum contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
Status, unknowns and future maturity are written out; color alone does not encode permission or eligibility.
Copy sits on opaque paper/white/dark fields, rather than uncontrolled photography overlays.
Captions/source details are 11–14px; body is 17px mobile. Small rights text is a known readability tradeoff requiring Founder inspection.
The static artboards contain no interactive semantic tree, alternative-text attributes, keyboard focus or actual target hit testing.

Installed Segoe UI regular/bold contain glyphs for `ქართული ბათუმი`; fontTools independently confirmed this coverage.
Georgia does **not** cover that tested Georgian string. H1's Georgia accent is English-only; any Georgian
heading must use a verified font/fallback and receive native review. This correction came from actual Independent QA.
Pillow's RAQM feature is unavailable. A rendered glyph specimen appears on the reference board, but Georgian shaping,
language completeness, translator/native-speaker acceptance and future webfont rights remain unverified.
No EN/KA switch or unapproved translation appears in visitor concepts.

Above-fold exports use 1440×900 and 390×844 viewports. Full pages include the complete story;
a fold crop may cut the beginning of the next section, as a viewport would, and never proves responsive behavior.
Image/photo panel geometry differs on mobile. No tiny phone shell shrinks the product copy.
Motion is absent. 320px stress, zoom/reflow, screen reader, keyboard, focus, safe areas, real-device performance
and public-user accessibility need separate authorized future work.

