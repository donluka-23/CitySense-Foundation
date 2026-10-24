"""Dependency-free static LANDING-WEB builder. No network, secrets, accounts or deployment."""
import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DEFAULT_OUTPUT = ROOT / "dist"
PHOTO = REPO / "docs/design/landing/assets/batumi-panorama.png"
PHOTO_SHA = "330e636d2ab7a56ff1d647616536e9a65eb883449d8de57a584eb64c7a0456ec"
PAGES = {"index": ("CitySense — city intelligence, beginning in Batumi", "Developing context-aware city intelligence and future agent-accessible local service infrastructure. Explore CitySense's Batumi vision and partner participation."), "partners": ("For Business & Partners — CitySense", "Explore proposed service and distribution participation in CitySense's first Batumi tourist use case. No guaranteed leads or live partner portal."), "contact": ("Contact — CitySense", "CitySense contact availability and proposed enquiry guidance. Real contact details appear only after confirmation."), "privacy": ("Privacy Policy — CitySense", "Privacy information for this informational CitySense website: no accounts, forms, analytics, advertising pixels or tracking features."), "terms": ("Website Terms — CitySense", "Terms for CitySense's informational vision website. Illustrative examples do not provide recommendations, bookings or operational services."), "affiliate-disclosure": ("Affiliate Disclosure — CitySense", "CitySense's current affiliate status and planned commission transparency. No affiliate links or provider acceptance is claimed.")}


def esc(value):
    return html.escape(str(value), quote=True)


def load_config(path=None):
    config = json.loads((ROOT / "site.config.example.json").read_text("utf8"))
    if path:
        provided = json.loads(Path(path).read_text("utf8"))
        unknown = set(provided) - set(config)
        if unknown:
            raise ValueError("Unknown configuration keys")
        for group, value in provided.items():
            if isinstance(config[group], dict):
                if not isinstance(value, dict) or set(value) - set(config[group]):
                    raise ValueError("Unknown or malformed configuration fields")
                config[group].update(value)
            else:
                config[group] = value
    for group in ["operator", "contact", "releaseReview"]:
        for key, value in config[group].items():
            expected = bool if key in {"founderAuthorized", "mailboxVerified"} else str
            if type(value) is not expected:
                raise ValueError("Wrong configuration field type")
    if not isinstance(config["publicOrigin"], str):
        raise ValueError("publicOrigin must be text")
    origin = config["publicOrigin"]
    if origin:
        parsed = urlsplit(origin)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
            raise ValueError("publicOrigin must be an HTTPS origin without credentials or a path")
        config["publicOrigin"] = origin.rstrip("/")
    email = config["contact"]["email"]
    if email and (len(email) > 254 or not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", email)):
        raise ValueError("Malformed contact email")
    return config


def contact_active(config):
    c = config["contact"]
    return bool(c["email"] and c["founderAuthorized"] and c["mailboxVerified"] and c["retentionStatement"].strip())


def release_blockers(config):
    review = config["releaseReview"]
    missing = []
    if not config["publicOrigin"]:
        missing.append("Actual approved HTTPS publication origin")
    else:
        host = urlsplit(config["publicOrigin"]).hostname
        if host in {"localhost", "127.0.0.1"} or host.endswith((".invalid", ".example", ".test", ".localhost")) or host in {"example.com", "example.org", "example.net"}:
            missing.append("Publication origin is a reserved/test hostname")
    for key, message in [("founderPublicationApproval", "Separate Founder publication authorization"), ("hostingPrivacyStatement", "Reviewed actual host/log/recipient/retention/transfer facts"), ("legalApplicabilityDecision", "Recorded applicability decision for actual informational/commercial operator and model"), ("applicableDisclosureApproval", "Approved fact-matched public legal/disclosure text")]:
        if not review[key].strip():
            missing.append(message)
    # Registration/contact are conditional, not universal prerequisites for an informational demo.
    # Public review must decide which identity/language facts apply; never invent those facts here.
    if config["contact"]["email"] and not contact_active(config):
        missing.append("Configured contact not authorized/verified with retention information")
    return missing


def contact_panel(config):
    if not contact_active(config):
        return '<div class="contact-status"><h3>Contact channel not yet published</h3><p>CitySense is preparing its public contact details. There is no enquiry form or message submission on this website.</p></div>'
    email = config["contact"]["email"]
    # A plain mailto opens the visitor's email client; there is no website submission service.
    return '<div class="contact-status"><h3>Write to CitySense</h3><p>Email is handled outside this website. Please read the <a href="/privacy.html">privacy information</a> before writing.</p><a class="button mailto" href="mailto:' + esc(quote(email, safe="@.")) + '">' + esc(email) + ' <span aria-hidden="true">↗</span></a></div>'


def operator_block(config):
    labels = {"name": "Responsible operator", "legalForm": "Legal form, where applicable", "registrationNumber": "Registered identifier, where applicable", "address": "Public address", "jurisdiction": "Operator jurisdiction"}
    values = [(labels[k], v) for k, v in config["operator"].items() if v.strip()]
    if not values:
        return '<p class="release-status">Operator identity has not been confirmed for publication. This draft does not identify an incorporated company or a governing jurisdiction.</p>'
    return '<dl class="operator-details">' + ''.join('<dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd>' for k, v in values) + '</dl>'


def page_shell(key, body, config, release=False):
    title, description = PAGES[key]
    nav = ''.join('<a class="nav-' + name + '" href="' + href + '"' + (' aria-current="page"' if key == target else '') + '>' + label + '</a>' for name, href, target, label in [('home', '/', 'index', 'Home'), ('partners', '/partners.html', 'partners', 'For Partners'), ('contact', '/contact.html', 'contact', 'Contact')])
    banner = '' if release else '<aside class="review-banner" aria-label="Review status"><div class="wrap"><strong>Local review</strong> · Informational demo · Not published</div></aside>'
    origin = config['publicOrigin']
    canonical = origin + ('/' if key == 'index' else '/' + key + '.html') if origin and release else ''
    canonical_tags = '<link rel="canonical" href="' + esc(canonical) + '"><meta property="og:url" content="' + esc(canonical) + '">' if canonical else ''
    robots = 'index,follow' if release else 'noindex,nofollow'
    return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(title) + '</title><meta name="description" content="' + esc(description) + '"><meta name="robots" content="' + robots + '"><meta name="referrer" content="no-referrer"><meta property="og:type" content="website"><meta property="og:title" content="' + esc(title) + '"><meta property="og:description" content="' + esc(description) + '">' + canonical_tags + '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="wrap"><a class="brand" href="/" aria-label="CitySense home">citysense</a><nav class="nav" aria-label="Main navigation">' + nav + '</nav></div></header>' + banner + '<main id="main">' + body + '</main><footer class="site-footer"><div class="wrap footer-inner"><p><strong>citysense / developing city intelligence</strong></p><nav class="footer-links" aria-label="Footer navigation"><a href="/partners.html">For Partners</a><a href="/contact.html">Contact</a><a href="/privacy.html">Privacy Policy</a><a href="/terms.html">Terms</a><a href="/affiliate-disclosure.html">Affiliate Disclosure</a></nav><p class="footer-note">An informational demonstration of CitySense’s direction. The tourist pilot is in development; live recommendations, booking and public agent access are not available here.</p><p class="footer-note">No active affiliate links or confirmed partner relationships are represented. Any future commission relationship will need clear disclosure.</p><p class="credits">Historical Batumi photography: Alexabsent, <a href="https://commons.wikimedia.org/wiki/File:Batumi.png" rel="noopener noreferrer">Batumi.png</a>, December 2023, <a href="https://creativecommons.org/publicdomain/zero/1.0/" rel="noopener noreferrer">CC0 1.0</a>. Resized and cropped for display. No endorsement or present-day conditions implied.</p></div></footer></body></html>\n'


def home(config):
    return '''<section class="intro wrap" aria-labelledby="home-title"><p class="eyebrow">Pilot in development / CitySense vision</p><div class="hero-title"><h1 id="home-title">The city. The question.<br>The evidence between them.</h1><p class="lede">Developing context-aware city intelligence. Batumi is the first tourist use case.</p></div><div class="canvas"><p class="illustrative">Illustrative sequence · not a functioning product</p><div class="canvas-grid"><div><img class="city-photo" src="/assets/batumi-960.webp" srcset="/assets/batumi-480.webp 480w, /assets/batumi-960.webp 960w, /assets/batumi-1335.webp 1335w" sizes="(max-width:640px) calc(100vw - 80px), (max-width:1000px) 55vw, 710px" width="1335" height="612" fetchpriority="high" alt="Historical view of Batumi’s coastal skyline, with mountains behind the city"><p class="photo-caption">Batumi · December 2023 · Alexabsent / CC0 1.0 · display crop</p><div class="visitor-need"><p class="eyebrow">Representative visitor need</p><h2>An outdoor afternoon in Batumi.</h2><p>Step-free access is essential.</p></div></div><div class="evidence"><p class="eyebrow">Evidence questions</p><h2>What must be known?</h2><ul><li>Place and entrance facts</li><li>Source, age and usage rights</li><li>Service and permitted contact</li></ul><div class="hold"><strong>Access evidence missing → hold.</strong><p>No defensible option yet. Clarify or wait for evidence.</p></div></div></div><div class="canvas-bottom"><p>A / B comparison slots only after required checks.<br>Up to five alternatives, or fewer / none.</p><a class="button" href="#reasoning">Explore the concept <span aria-hidden="true">↓</span></a></div></div><p class="hero-sequence">Evidence → conditional comparison → permitted action → future authorized agents</p></section><section class="section wrap" id="reasoning" aria-labelledby="reasoning-title"><p class="eyebrow">The reasoning, revealed</p><h2 class="section-heading" id="reasoning-title">Context changes<br>what counts as an option.</h2><div class="reasoning-grid"><article class="step"><span class="number">02</span><div><h3>The essential constraint</h3><p>Step-free access is essential.</p><p>An unknown required fact cannot pass.</p></div></article><article class="step"><span class="number">03</span><div><h3>The evidence boundary</h3><p>Access evidence missing → hold.</p><p>Source, age, rights and unknowns matter. No current place evidence is connected to this illustration.</p></div></article><article class="step"><span class="number">04</span><div><h3>Comparison, when defensible</h3><p>Up to five eligible alternatives, or fewer.</p><p>A / B are conceptual slots only. No eligible option is asserted here.</p></div></article><article class="step"><span class="number">05</span><div><h3>An action with permission</h3><p>Permitted contact → partner response.</p><p>A future pathway, subject to verified channels and permissions. A request is not confirmation.</p></div></article></div></section><section class="section wrap" aria-labelledby="maturity-title"><p class="eyebrow" id="maturity-title">Where the work stands</p><div class="maturity-grid"><article><h3>Existing internal foundation</h3><p>Research, evidence and private information components. These do not establish public product readiness or validated accuracy.</p></article><article><h3>First tourist use case</h3><p>Batumi discovery and informed selection — in development. Closed-pilot participation is subject to separate permissions.</p></article><article><h3>Future infrastructure</h3><p>Governed services and authorized agent interfaces — not publicly available.</p></article></div></section><section class="vision" aria-labelledby="vision-title"><div class="wrap"><p class="eyebrow">Long-term vision / future direction</p><h2 id="vision-title">One governed foundation.<br>More than one interface.</h2><p class="connections">People ↔ places ↔ local services ↔ authorized AI agents</p><div class="vision-points"><p>Source-governed evidence</p><p>Constraints and human choice</p><p>Permitted services and agent access</p></div><p class="future-label">Future vision · not an operating city network</p></div></section><section class="section wrap invitation" aria-labelledby="invitation-title"><p class="eyebrow">A small website. A specific invitation.</p><h2 id="invitation-title">Help shape the first<br>Batumi use case.</h2><p class="lede">Service providers and distribution partners can explore bounded participation. Terms, placement permissions and contact channels remain to be agreed.</p><a class="button" href="/partners.html">Explore partner paths <span aria-hidden="true">↗</span></a></section>'''


def partners(config):
    return '''<section class="page-intro wrap" aria-labelledby="partners-title"><p class="eyebrow">Pilot in development / For Business &amp; Partners</p><h1 id="partners-title">Local services,<br>understood in context.</h1><p class="lede">CitySense is developing contextual discovery in Batumi. We are exploring participation with service providers and distribution partners.</p><div class="status-panel"><p class="eyebrow">Founding Partner participation / proposed</p><p>No commitments, guaranteed leads or working portal.</p></div><div class="partner-paths"><article class="partner-path"><p class="eyebrow">01 / Service Partners</p><h2>Meet relevant visitor needs responsibly.</h2><p>Tours and activities, paid attractions, sports facilities and eligible local services. Private drivers and transfers are prospective categories.</p><p>A proposed participation path: explain service facts, evidence rights and permitted contact. Actual categories and partners remain to be approved.</p></article><article class="partner-path"><p class="eyebrow">02 / Distribution Partners</p><h2>Explore contextual discovery for your guests.</h2><p>Hotels, apartments and other accommodation. Potential airport-area commercial touchpoints are subject to permissions and agreed incentives.</p><p>Agree placement, audience, referral terms and responsibilities before a bounded test. No placement or conversion improvement is promised.</p></article></div></section><section class="section wrap" aria-labelledby="value-title"><p class="eyebrow" id="value-title">The proposed value path / not live</p><div class="value-path"><div><span class="number">01</span><h3>Tourist need</h3></div><div><span class="number">02</span><h3>Eligibility before suitability</h3></div><div><span class="number">03</span><h3>Relevant business</h3></div><div><span class="number">04</span><h3>Permitted contact or request</h3></div><div><span class="number">05</span><h3>Partner response</h3></div></div><p class="bounded-note">Required evidence and permissions first. A request is not confirmation; partner response and fulfillment remain separate.</p></section><section class="section wrap" aria-labelledby="interest-title"><div class="partner-contact"><p class="eyebrow">Express interest / proposed participation</p><h2 id="interest-title">Help shape the first Batumi use case.</h2><p class="lede">An initial conversation would identify your business, service or distribution path, one preferred reply channel and an optional short description. An enquiry would not establish a partnership or listing.</p>''' + contact_panel(config) + '''<a class="button" href="/contact.html">View contact information <span aria-hidden="true">↗</span></a><p class="release-status">No form or submission service is enabled. Please do not send customer data, identity documents, payment details or credentials.</p></div></section><section class="section wrap" aria-labelledby="onboarding-title"><p class="eyebrow" id="onboarding-title">A bounded onboarding outline / proposed</p><ol class="onboarding"><li>Introduction and participation path</li><li>Identity, evidence rights and permission review</li><li>Service facts and contact rules</li><li>Participation terms and a separately authorized test</li></ol></section><section class="vision" aria-labelledby="partner-vision"><div class="wrap"><p class="eyebrow">Future / agent-accessible services</p><h2 id="partner-vision">Evidence and permission,<br>beyond a single channel.</h2><p class="connections">Authorized AI-agent discovery is a future direction, not an operating partner capability. There is no public API or MCP access offered here.</p></div></section><div class="section wrap"><p class="bounded-note">Affiliate programmes may support an initial supply strategy after separate authorization. They do not define CitySense’s longer-term identity or provide permission for paid priority in suitability.</p></div>'''


def contact(config):
    return '<section class="contact-page wrap" aria-labelledby="contact-title"><p class="eyebrow">CitySense / contact</p><h1 id="contact-title">Start a conversation.</h1><p class="lede">CitySense is preparing an initial informational website for its Batumi vision and prospective partner participation.</p>' + contact_panel(config) + '<h2>For potential partners</h2><p>When a verified contact channel is available, a short introduction can describe your business, service or distribution path and one preferred reply channel. No enquiry is collected here.</p><h2>Privacy and sensitive information</h2><p>Read our <a href="/privacy.html">privacy information</a>. Please do not send customer information, identity documents, payment details, passwords or sensitive personal information.</p><h2>Current scope</h2><p>This website does not accept service orders, bookings or payments. An introduction is not confirmation of partnership, availability or fulfillment.</p>' + operator_block(config) + '</section>'


def legal_page(title, sections, config, release=False):
    notice = '<aside class="draft-notice"><p><strong>Policy draft · 11 October 2026.</strong> This document describes the local informational preview. Public hosting and operator details are not yet finalized.</p></aside>' if not release else ''
    toc = '<nav class="contents" aria-label="Page contents"><ul>' + ''.join('<li><a href="#' + key + '">' + esc(heading) + '</a></li>' for key, heading, _ in sections) + '</ul></nav>'
    extra = config['releaseReview']['georgianDisclosureText']
    georgian = '<section lang="ka"><h2>ინფორმაცია ქართულად</h2><p>' + esc(extra) + '</p></section>' if release and extra.strip() else ''
    return '<article class="legal wrap"><p class="eyebrow">CitySense / website information</p><h1>' + esc(title) + '</h1>' + notice + toc + ''.join('<section id="' + key + '"><h2>' + esc(heading) + '</h2>' + body + '</section>' for key, heading, body in sections) + georgian + '</article>'


def legal_sections(config, release=False):
    hosting = config['releaseReview']['hostingPrivacyStatement'].strip()
    contact_copy = '<p>No public mailbox is connected. No enquiry form or message submission service is enabled.</p>'
    if contact_active(config):
        contact_copy = '<p>A contact link opens your own email client. If you choose to send a message, sender details and message content are used to answer your enquiry outside this website. Please do not send sensitive personal information.</p><p>' + esc(config['contact']['retentionStatement']) + '</p>'
    host_copy = '<p>This local preview receives browser requests to serve pages and assets. Its preview server does not retain access logs or store submitted messages. Network metadata is still processed transiently to deliver responses.</p><p>Public hosting has not been selected. Its actual logging, security processing, recipients, retention and any international transfers must be reviewed and disclosed before publication.</p>' if not release else '<p>' + esc(hosting) + '</p>'
    privacy = [('scope', 'Scope and responsible operator', '<p>This notice describes CitySense’s informational vision website. It is separate from any future tourist application or partner service.</p>' + operator_block(config)), ('collection', 'Website features and data', '<p>The website has no accounts, enquiry forms, analytics, advertising pixels, embedded third-party services or booking functions. Its own pages set no cookies and use no browser storage or tracking features.</p><p>All images and styling are served locally with system fonts. No third-party resource is loaded automatically. Following an external source link takes you to a separate website.</p>'), ('hosting', 'Technical requests and hosting', host_copy), ('contact', 'Contact and enquiries', contact_copy + '<p>Any future contact process must specify the responsible recipient, lawful purpose and basis, necessary retention and deletion arrangements, relevant processors and transfers. There is no marketing opt-in or mailing list here.</p>'), ('rights', 'Privacy requests and rights', '<p>No account profile or submitted enquiry is retained by this preview website. Once public processing is established, information will explain applicable access, correction, deletion, restriction, portability and consent rights, how to contact the responsible operator, and any lawful limitations.</p><p>Where Georgian personal-data law applies, the competent supervisory authority is the State Audit Office of Georgia. An actual controller and rights-request contact must be identified for relevant public processing; this draft does not establish those facts.</p>'), ('links', 'External links and changes', '<p>External sites have their own privacy notices and processing practices. No affiliate links are active here. This notice must be updated before introducing hosting-dependent processing, email handling, tracking or new services.</p>')]
    terms = [('purpose', 'Purpose and development status', '<p>CitySense is developing context-aware city intelligence and agent-accessible local service infrastructure, beginning with Batumi tourist discovery. This website explains that direction. The tourist pilot and partner participation remain in development.</p>'), ('illustrations', 'Illustrative information', '<p>Example decision states are explanatory illustrations. They do not provide live recommendations or establish that a location or service satisfies accessibility, safety or suitability requirements. Required evidence that is missing cannot be treated as satisfied.</p><p>Historical photography identifies a city context, not present conditions, routes, weather, availability or access facts. Scores and model accuracy are not represented as validated.</p>'), ('services', 'No orders, bookings or commitments', '<p>This website does not accept reservations, payments or service orders. It provides no booking confirmation or service fulfillment. Proposed partner participation and future agent access require separate agreement and authorization.</p><p>An enquiry does not establish a partnership, approved listing, booking or access to an API. No guaranteed acquisition or conversion improvement is promised.</p>'), ('rights', 'Content and third-party material', '<p>Material must not be represented as confirmed inventory, current availability, validated scoring or an established commercial relationship. Relevant photographic credits identify the original creator, source and license. Other third-party material remains subject to its own rights.</p><p>External websites control their own content and terms. This site does not endorse a provider or promise the accuracy or availability of its separate services.</p>'), ('limits', 'Rights and responsibility', '<p>These informational terms do not limit rights that applicable law does not permit to be limited. They do not establish a seller, merchant-of-record arrangement, incorporated entity, exclusive court or selected governing jurisdiction.</p>'), ('operator', 'Operator and enquiries', operator_block(config) + '<p>Actual operator and contact details will be published when confirmed, as applicable to the eventual informational or commercial model. See <a href="/contact.html">contact information</a> and the <a href="/privacy.html">privacy notice</a>.</p>')]
    affiliate = [('current', 'Current status', '<p>CitySense is exploring affiliate distribution as a possible future supply and monetization strategy. This website contains no active affiliate links and makes no claim of acceptance by, endorsement from or integration with any affiliate provider.</p>'), ('future', 'Future commission transparency', '<p>If authorized affiliate links are introduced, they will be identified where encountered, with an explanation that a qualifying purchase may generate a commission. A footer disclosure alone will not replace a clear notice beside a promoted affiliate link.</p><p>The actual commercial arrangement and provider terms must be reviewed before any claim about prices, commission or cost to a visitor. No rate or “no extra cost” assurance is stated here.</p>'), ('bookings', 'Provider transactions', '<p>Any future booking completed on a provider’s website would be governed by that provider’s terms and confirmed by the authorized party. An affiliate link is not booking confirmation or proof of service availability. This website accepts no payments.</p>'), ('independence', 'Evidence and suitability', '<p>Eligibility and evidence precede suitability. No commercial priority or paid ranking is active. A commission relationship does not itself establish that a service meets a visitor’s needs.</p>'), ('questions', 'Questions and changes', '<p>See the truthful <a href="/contact.html">contact status</a>. This disclosure must be updated before any affiliate relationship or monetized link is activated.</p>')]
    return {'privacy': privacy, 'terms': terms, 'affiliate-disclosure': affiliate}


def build(config=None, output=DEFAULT_OUTPUT, release=False):
    config = config or load_config()
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents and output.name != 'dist' or REPO == output or output in REPO.parents:
        raise ValueError('Output must be the app dist folder or a separate temporary directory')
    blockers = release_blockers(config)
    if release and blockers:
        raise ValueError('Public artifact preparation blocked: ' + '; '.join(blockers))
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'assets'; assets.mkdir(exist_ok=True)
    for p in (ROOT / 'assets').iterdir():
        if p.is_file():
            shutil.copyfile(p, assets / p.name)
    sections = legal_sections(config, release)
    bodies = {'index': home(config), 'partners': partners(config), 'contact': contact(config)}
    for key, title in [('privacy', 'Privacy Policy'), ('terms', 'Website Terms'), ('affiliate-disclosure', 'Affiliate Disclosure')]:
        bodies[key] = legal_page(title, sections[key], config, release)
    for key, body in bodies.items():
        (output / (key + '.html')).write_text(page_shell(key, body, config, release), encoding='utf8')
    robots = 'User-agent: *\nDisallow: /\n' if not release else 'User-agent: *\nAllow: /\nSitemap: ' + config['publicOrigin'] + '/sitemap.xml\n'
    (output / 'robots.txt').write_text(robots, encoding='utf8')
    urls = [] if not release else [config['publicOrigin'] + ('/' if k == 'index' else '/' + k + '.html') for k in PAGES]
    (output / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + esc(u) + '</loc></url>' for u in urls) + '</urlset>\n', encoding='utf8')
    files = {p.relative_to(output).as_posix(): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'build-manifest.json'}
    manifest = {'mode': 'approved-public-artifact' if release else 'local-preview', 'pages': list(PAGES), 'files': files, 'contact_active': contact_active(config), 'release_blockers': blockers, 'no_deployment_performed': True}
    (output / 'build-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', help='Explicit reviewed factual JSON; never reads .env or credentials')
    parser.add_argument('--release', action='store_true', help='Prepare approved public files only; does not deploy')
    parser.add_argument('--check-readiness', action='store_true')
    args = parser.parse_args(); config = load_config(args.config)
    if args.check_readiness:
        blockers = release_blockers(config)
        print(json.dumps({'status': 'BLOCKED' if blockers else 'PREPARED', 'blockers': blockers, 'identity_requirements': 'conditional applicability; no universal incorporation prerequisite'}, indent=2))
        return 2 if blockers else 0
    result = build(config, release=args.release)
    print(json.dumps({'mode': result['mode'], 'pages': len(result['pages']), 'files': len(result['files']), 'bytes': sum(v['bytes'] for v in result['files'].values()), 'contact_active': result['contact_active']}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
