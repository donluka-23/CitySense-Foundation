# Visual decisions — proposals for Founder inspection

Date 2026-10-11, revision landing-ux0-r1. Hybrid direction was selected by the Founder; these layouts/content are not accepted.
Product evidence was recovered from Blueprint v0.4, STATUS and protected map reports before composing concepts.
The tourist discovery wedge stays first. Future city intelligence connects people, places, services and authorized agents through governed interfaces.

The three compositions share the headline “Discover a city with context.”, pilot status, honest CTA,
constraint-first journey, same three maturity labels and future ecosystem. H1 uses editorial serif headings as a scoped accent;
H2/H3 emphasize the shared sans serif. This is an option to judge, not a replacement brand system.

| Element | Design proposal / purpose |
|---|---|
| Palette | Paper #F5F2EA, ink #172D32, supporting #4C6264, sea-glass accent #21675F; dark field confined to future-platform section. |
| Typography | Segoe UI body/interface; desktop headings 40–66px, body 18–22px; mobile hero 40/45, section 31–32/37–38, body 17/26. H1 hero Georgia 66 desktop / 40 mobile, English-only accent: tested Georgian glyphs absent; fallback required. |
| Grid | Desktop 1440 with 120px gutters / 1200px content; mobile 390 with 24px gutters / 342px content. Mobile is separately composed, not shrunk desktop. |
| Spacing | 8/12/16/24/32/48/64/96px vocabulary, generous section breaks; open editorial fields and divider lists rather than repeated icon cards. |
| CTA | 48px-high primary “See how it will work”; static proposed scroll action. No live-product, booking, signup or enquiry submission. |
| Navigation | Desktop vision/how/partners sections; mobile wordmark plus vision entry; no unexplained hamburger or unapproved EN/KA control. |
| Product illustration | Example request, explicit unknown access/eligibility, two illustrative alternatives, conspicuously nonfunctional map surface. No valid inventory or current selection results asserted. |
| Readiness | Existing internal foundation / pilot being developed / long-term vision, with words as well as color. No implication of a public API or operational agent network. |
| Distribution | Accommodation QR pilot proposed; permissions pending. No actual QR destination or committed apartment/airport partner. |
| Partner/footer | Enquiry channel awaiting verification; publisher/contact/privacy/terms pending; no fabricated policy or legal entity. Future affiliate option remains inactive. |

Intended later journey: authorized QR entry → need/constraints → up to five defensible alternatives (or fewer/none/clarification)
→ compare → inspect map/evidence → informed selection → only supported actions. Landing depicts the explanation,
not every integrated product state. No ranking, booking or /v1 change follows from these drawings.

PWA reuse is an opportunity for type/spacing/status/evidence hierarchy; no fixed application architecture or implementation component contract is created.
Motion is absent. Any later motion would need reduced-motion behavior. Keyboard, screen reader, browser, safe area and device tests need separately authorized implementation.

Production tools: installed Pillow, installed Windows fonts, installed fontTools and already-bundled Poppler.
No external installation or experimental feature. PNG artboards are rendered at 2× and downsampled to exact viewport width.
Raster PDF companions use the 2× drawing at 144dpi; existing Poppler re-renders them at 72dpi for dimension/visual checks.
The initially intended ReportLab path was unavailable. The approved PNG/PDF alternative uses no website code.
Static drawing helper is [.local/landing-ux0/render_artboards.py](../../../.local/landing-ux0/render_artboards.py), local ignored tooling; PDFs are raster, not editable vectors.
Run `python -B .local/landing-ux0/render_artboards.py` from the repository with the existing environment, after checking scope.
It redraws design exports only; it does not run a server, use a provider or modify product code.

