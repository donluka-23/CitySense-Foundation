# Telegram demonstration contract — Sprint 3

Telegram is a deterministic interface adapter over the existing authenticated CitySense REST
service. There is no second engine, chatbot model, supplier discovery, booking, payment or public
webhook. Private polling is executable but has **not been activated**. No Telegram credentials or
real users were used. Offline transcripts and application construction exercise local behavior.

Commands: /start explains mode and limitations; /help gives syntax; /needs lists supported needs;
/places lists at most five operator-selected research IDs; /evaluate selects a need, defined zoned
time, walking budget and one to three IDs with caller estimates; /near accepts coordinates with
the same need/time/budget and an explicitly estimated walk duration. /sports is an honest future
acceptance fixture reporting absent courts/weather/routes/availability. Unsupported free text and
Telegram location shares return guidance; location shares are not retained or silently interpreted.
The coordinate command supplies a location directly; verified entrance selection awaits site review.

`/evaluate quiet_rest 2026-10-10T19:00:00+04:00 30 PLACE_ID:20 PLACE_ID_2:25`

Candidate IDs may contain colons: the last colon separates the walking estimate. Times need a
timezone, must be future/current and no more than seven days ahead. Hard walking bounds, duplicate
IDs and finite coordinates/estimates are validated before scoring. Coordinate search radius is 2 km;
the shared API returns at most 30 records, restricted again to the operator's selected universe.

| Mode | Allowed evidence | User-facing behavior |
|---|---|---|
| real | Stored non-synthetic sources with research and redistribution permission | Up to three scored options or honest abstention/rights denial; geometry remains source-reported |
| synthetic | Stored fictional sources, explicitly synthetic metadata | Every reply says SYNTHETIC DEMO and no current Batumi facts; no purported verified map links |

Mode checks apply to place and feature metadata. Mixing modes fails closed. The current real OSM
inventory is local-research only, so /places and /evaluate in real mode return a rights denial.
The adapter cannot request the new local-research audience or read the database directly. Source
publication remains a gate even for an authorized Telegram operator. There are no currently
independently field-verified research sites; map links for a future permitted real source clearly
label source-reported coordinates rather than claiming verified entrances.

Replies include explicit target, model version, unvalidated index, main components/reasons,
exclusions, freshness or missing environmental evidence, walking-estimate warning and unknown
operating availability. Rank display is capped at three. Geometry retrieval timestamps appear in
/places. An insufficient-data reply is a valid result, not a recommendation. No current feed or
bookability is inferred from entity existence. Text replies use plain text and disable link previews;
source names are bounded and no model can manufacture candidate IDs or observations.

Security/privacy: static private-user allowlist (1–50), place allowlist (1–5), private chats only,
default six accepted requests/minute/user, 1024-byte input, 256 KiB operator response, 3900-character
reply, five-second REST phase timeout and twenty-second dispatch deadline. The polling queue caps
at 100 and handlers run sequentially. Authorized user IDs remain only in process configuration/counts;
no user_data store, chat/content/location archive or analytics exists. Library logs that could expose
token-bearing Telegram URLs are discarded; error logs contain only a constant redacted message.
Future studies must not repurpose this demo as a participant collection channel without review.

OperatorHTTPBackend requires loopback HTTP and a configured key of at least 32 characters; routes
are fixed, identifiers validated, redirects/proxy environment disabled. Existing API key, city/scope,
read-only transaction and source rules apply. Environment secrets are never inserted into receipts.
This is a local private demonstration, not multi-user authorization, shared quotas or a production
identity gateway. Telegram itself receives messages if polling is later enabled; local nonretention
does not assert anything about Telegram's storage policy.

Dependency reviewed: [python-telegram-bot 22.8](https://docs.python-telegram-bot.org/en/stable/) is
compatible with the locked HTTPX 0.28.1 dependency and uses LGPL-3. The unchanged upstream library
is dynamically used; notices/licence remain installed. No optional webhook/job/agent dependencies
were added. Locked-package advisory scan is retained, not an assurance against undisclosed issues.
No transport call, paid model call or operational cost was observed. Hosting/network/provider costs
require a measured later private trial. See [setup](TELEGRAM_SETUP.md) and [acceptance](END_TO_END_ACCEPTANCE.md).
