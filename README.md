# Iryna's Green Space

Website template for a refill shop, eco laundry, sound therapy room and safe
space.

Built with [Jekyll](https://jekyllrb.com/) on the
[al-folio](https://github.com/alshedivat/al-folio) theme (MIT), adapted from
[hdclark94.github.io](https://github.com/HDClark94/hdclark94.github.io).

**This is a template.** The structure, styling and artwork are finished; the
words and the facts are placeholders. Everything that needs replacing is either
marked _to be confirmed_ on the page or left as an HTML comment in the source
with a prompt explaining what belongs there. Comments are stripped when the site
builds, so they never appear to visitors.

## Editing the words

Everything is a plain text file. No code required to change the content.

| What                               | File                 |
| ---------------------------------- | -------------------- |
| Home page, the vision, the values  | `_pages/about.md`    |
| Opening hours, address, contact    | `_pages/visit.md`    |
| The four offerings                 | `_offerings/`        |
| Shop stock and prices              | `_data/products.yml` |
| Short updates on the home page     | `_news/`             |
| Site name, contact links, settings | `_config.yml`        |

Each file starts with a block between `---` lines. That's settings. Everything
below it is the page text, written in Markdown — `**bold**`, `_italic_`,
`## heading`, and `- ` for bullets.

### Adding an update

Copy a file in `_news/`, give it a new name, change the date and the text. It
appears on the home page automatically, newest first.

### Adding or reordering an offering

Copy a file in `_offerings/`. The `order:` number sets where it appears, and
`image:` points at a tile in `assets/img/offerings/`. The `status:` line is the
small pill on the card — use it for "Open", "By appointment", "Coming soon".

## Before it goes live

- [ ] Replace every _to be confirmed_ on `_pages/visit.md`
- [ ] Fill in contact details in `_config.yml` — icons appear automatically
- [ ] Set `url:` in `_config.yml` to the real domain
- [ ] Rewrite the vision on the home page in Iryna's own voice
- [ ] Swap the leaf artwork for photographs, if there are any (see below)

## Map

A map sits in the footer, to the right of the copyright, on every page. It is
configured under `map:` in `_config.yml`. **The coordinates are a placeholder — Tavira in the Algarve.**
Replace `lat` and `lng` with the real address before launch: right-click the
spot in Google Maps and the coordinates are the first item in the menu.

`provider` accepts `google` or `osm`. Either way the embed is **gated behind
consent** — see below. Switching to `osm` needs no API key and sends far less
to a third party, which makes the consent question less fraught.

Set `enabled: false` to remove the map entirely.

## Cost breakdowns

Every product on the shop page opens a **Where your money goes** panel showing
what reaches the maker, shipping and import, VAT, card fees and the shop.

The figures live in `_data/products.yml` as absolute amounts, not percentages,
so they can be checked rather than taken on trust. `scripts/check_products.py`
verifies that every breakdown sums to its price to the cent and that any VAT
line matches the configured rate — and it runs in CI, so a wrong figure fails
the build instead of quietly misleading a customer. That check is the feature;
the panel is just how it is displayed.

**VAT is computed from the gross price:**

```
vat = gross × rate / (100 + rate)
```

Not `gross × rate/100`. At 23% that difference is about a fifth of the tax line,
and on a page about honesty it would be a bad place to slip. The check enforces
the correct formula.

`vat_rate` in `_config.yml` is **23** — Portugal mainland. The UK is 20, and
Madeira and the Azores differ. Change it there and update the figures; the check
will tell you if they no longer agree.

Segment colours are validated categorical slots checked against this site's own
tan and soil backgrounds, not the defaults. Several pairs that look distinct to
full colour vision collapse under deuteranopia, so if you swap them for prettier
earth tones, re-run the validator rather than trusting your eye. The table under
the bar carries a figure and a swatch on every row, so identity never rests on
colour alone.

## Consent and cookies

The site is built to operate in the EU, which means third-party content must not
load until the visitor agrees.

The important part is _where_ that is enforced. `_includes/map.liquid` renders a
**placeholder**, not an iframe — it carries the embed URL in a `data-consent-src`
attribute, and `assets/js/consent.js` only builds the real iframe after a
decision. A banner shown over an already-loading embed would be worthless: by
then the provider has the visitor's IP and has set its cookies. If you add any
other third-party embed — a video, a social feed, a Stripe Buy Button — put it
behind the same attribute rather than dropping an iframe straight into a page.

Accept and Reject are deliberately the same size and weight. Regulators have
repeatedly found that making refusal harder than acceptance invalidates the
consent collected.

The decision is stored in local storage as `igs.consent.v1`, and can be changed
from **Cookie settings** in the footer. Storing the answer does not itself need
consent: it exists only to honour the choice.

What the site stores, and why none of it needs consent:

| Key              | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| `igs.consent.v1` | Remembers the answer above                         |
| `theme`          | Light or dark mode, if the visitor uses the toggle |

There is no analytics, no advertising and no tracking on this site. If you add
analytics later, it must go behind the same gate, and the privacy page needs
updating to say so.

### The policy pages are drafts

`_pages/privacy.md` and `_pages/terms.md` are written against how the site
actually behaves, and cover the headings EU rules require — but **they are
drafts and have not been reviewed by anyone qualified.** Every place needing a
real answer is marked _to be confirmed_: the trading entity, the supervisory
authority, VAT treatment, delivery terms, who pays return postage, and record
retention. Have them checked before taking the first order. An incomplete
privacy notice is itself a breach.

## Payments

The shop takes payment through **Stripe Payment Links**. Checkout happens on a
page hosted by Stripe, which is what makes this work on a static site at all:
Apple Pay's own JavaScript API needs a server to validate a merchant session
with Apple on every transaction, and GitHub Pages has no server. Going through
Stripe's hosted checkout sidesteps that entirely — Apple Pay, Google Pay and
cards all work, with no backend and no domain verification.

To start selling an item:

1. In the Stripe Dashboard, create a **product** and then a **Payment Link** for it
2. Copy the link (it looks like `https://buy.stripe.com/xxxx`)
3. Paste it into that item's `checkout_url` in `_data/products.yml`
4. Set the real `price` in the same file — Stripe holds the figure that is
   actually charged, so **these two must be kept in step by hand**

Items with a blank `checkout_url` show "Ask in store" rather than a buy button,
so stock can be listed before it is set up to sell online.

Apple Pay appears automatically at checkout for anyone on an Apple device with a
card in Wallet. Nothing needs enabling in this repository for that.

### Before taking the first payment

- [ ] A returns policy on the shop page — UK and EU distance selling generally
      gives customers 14 days to change their mind
- [ ] Delivery and collection terms
- [ ] Whether VAT applies, and whether prices include it
- [ ] A privacy notice covering Stripe as a payment processor

### If you ever want the pay button on this site rather than Stripe's page

That needs Stripe Elements and a server to validate the Apple Pay merchant
session, so GitHub Pages would no longer be enough. You would also have to serve
Stripe's verification file at `/.well-known/apple-developer-merchantid-domain-association`
— `.well-known` is already listed in `include:` in `_config.yml`, because Jekyll
skips dot-directories by default and would otherwise drop the file silently.

## Artwork

Every image is generated by [`scripts/artwork.py`](scripts/artwork.py) — the
banner, the logo, the favicon and the four offering tiles. No stock photos, no
licensing to worry about.

```bash
pip install -r scripts/requirements.txt
make art
```

Colours and shapes are a few lines near the top of the script. To swap in real
photographs instead, see [`scripts/README.md`](scripts/README.md).

## Running it locally

Needs Ruby 3.x and [ImageMagick](https://imagemagick.org/).

```bash
bundle install
make serve        # http://localhost:4000
```

Run `make` on its own to list every command.

## Publishing

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the
site and publishes it to the `gh-pages` branch. Then turn on GitHub Pages in the
repository settings, serving from `gh-pages`.

**One setting depends on the repository name.** If the repo is named
`<username>.github.io`, leave `baseurl:` blank in `_config.yml`. If it has any
other name — so the site lives at `<username>.github.io/irynas-green-space` —
set `baseurl: /irynas-green-space`. Getting this wrong makes every link and
image 404, and it is the single most common first-deploy problem.

A custom domain needs a `CNAME` file in the repository root containing just the
domain, and `baseurl:` left blank.

## Gotchas

- **Don't post-date anything.** Jekyll silently refuses to build a page dated in
  the future — the link appears but the page 404s, and the build still passes.
- `scripts/` and `Makefile` are excluded from the published site.
- Dark mode is on. Anything baked into an image can't follow it, which is why
  the banner has light and dark versions; the tiles and logo use mid-tone greens
  that work on both.
