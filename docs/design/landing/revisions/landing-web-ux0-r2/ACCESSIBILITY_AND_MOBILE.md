# Accessibility and mobile review scope

Review artifacts are native 1440/390 PNGs and raster PDFs, not browser screenshots or working UI.
Above-fold crops are 1440×900 and 390×844. Long artboards must be reviewed at native width or in crops;
an overview thumbnail cannot establish mobile readability.

Design targets: 24 mobile margins, 342 content width, 48-high CTAs; core mobile body generally 15–17 with 23–26 leading.
Supplementary attributions/status use smaller text and must be reconsidered for publication, especially long source URLs.
Missing required evidence has a literal hold and explanatory text, never color alone. Future/illustrative labels remain adjacent to claims.
Do not rely on photograph contrast: core text is on opaque paper/white/ink surfaces.
Mobile reading order is context → need → essential fact/unknown → conditional comparison → permission-bound action → future agents.
Later steps may follow the fold; the need/essential access/hold are visible in all three initial mobile viewport details.

The [verification receipt](evidence/VERIFICATION.json) records actual sRGB contrast calculations for all text token pairs,
plus font glyph checks. Contrast values apply to flat tokens, not a whole-site WCAG certification.
Rules/surfaces need their own future focus/control contrast treatment; no raster artwork proves interactive semantics.

Segoe UI regular/bold contain tested Georgian Mkhedruli glyphs. Georgia does not; its use is English-only in S1.
No Georgian translation, multilingual toggle, shaping QA or local-language acceptance is claimed.
Pillow has no RAQM support in this environment; glyph coverage is not localization validation.
Typeface redistribution/webfont rights have not been established; exported raster artifacts contain no font binaries.

Three complete stationary desktop/mobile storyboards are the actual reduced-motion alternatives.
Every state and qualification remains visible without animation. Timed GIFs are optional review previews,
not an autoplay requirement or production implementation; proposed durations are in [rationale](VISUAL_RATIONALE.md).

Not executed: 320-width reflow, physical devices, touch targets in a browser, 200% zoom, keyboard/focus navigation,
screen reader, contrast on a deployed page, reduced-motion media query, browser performance/network budgets or real form validation.
These are later acceptance checks under separate execution and Founder approval, not failures of static UX-0 export integrity.
No PRODUCT-APP accessibility or UX approval is inherited.
