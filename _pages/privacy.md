---
layout: page
permalink: /privacy/
title: privacy
description: What this site stores, what it sends elsewhere, and what it does not do.
nav: false
---

<!--
  DRAFT. The structure and the technical facts below are accurate for the site
  as built, but this has not been reviewed by anyone qualified. Before trading,
  have it checked and fill in the controller details - an incomplete privacy
  notice is itself a breach.
-->

_Last updated: {{ site.time | date: "%-d %B %Y" }}. **Draft — not yet reviewed.**_

## Who is responsible

<!-- Required: trading name, legal entity if any, postal address, contact email.
     If you appoint a Data Protection Officer, name them. Most small shops do not
     need one, but you must give a contact point for data questions. -->

_To be confirmed._

## The short version

This site has no analytics, no advertising, no tracking pixels and no social
media embeds. It sets no cookies of its own. Fonts are served from this site
rather than from Google.

Two things are worth knowing about in detail: the map, and payments.

## What is stored on your device

| What             | Why                                                | Needs consent?                            |
| ---------------- | -------------------------------------------------- | ----------------------------------------- |
| `igs.consent.v1` | Remembers whether you allowed the map to load      | No — it exists only to honour your answer |
| `theme`          | Remembers light or dark mode if you use the toggle | No — a preference you set yourself        |

Both are browser local storage, not cookies, and neither leaves your device.
Clearing site data removes them.

## The map

The map at the foot of each page is embedded from
{% if site.map.provider == "osm" %}OpenStreetMap{% else %}Google Maps{% endif %}.
**It does not load until you allow it.** If you accept, your IP address and
browser details are sent to them and they may set their own cookies, under their
privacy policy rather than this one. If you reject, nothing is requested and you
see a placeholder with a link you can open yourself.

You can change the answer at any time with **Cookie settings** in the footer.

## Payments

Payment is handled by **Stripe**, on Stripe's own pages. Card details are never
entered on this site and never reach us. Stripe processes your payment data as a
controller in its own right; see Stripe's privacy policy.

We receive from Stripe only what is needed to fulfil an order — name, delivery
address, what was bought, and whether it was paid.

## Server logs

This site is hosted on GitHub Pages. GitHub records standard request logs,
including IP addresses, for security and operational reasons. We have no access
to them.

## Your rights

Under the GDPR you may request a copy of your data, ask for it to be corrected
or erased, object to processing, or complain to a supervisory authority.

<!-- Name the relevant authority: for Portugal, the CNPD. -->

_Contact details and supervisory authority to be confirmed._

## How long things are kept

<!-- Order records usually have to be kept for tax purposes - commonly 6 to 10
     years depending on the country. Check the local requirement and state it. -->

_To be confirmed._
