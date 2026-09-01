#!/usr/bin/env python3
"""Build every Finbolt page from one shared shell so the design stays identical."""

import os, re

OUT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
def svg(body, box="0 0 24 24", stroke=True):
    attrs = ('viewBox="%s" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"' % box) if stroke else \
            ('viewBox="%s" fill="currentColor"' % box)
    return '<svg xmlns="http://www.w3.org/2000/svg" %s aria-hidden="true">%s</svg>' % (attrs, body)

I = {
  "bolt":    svg('<path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/>', stroke=False),
  "arrow":   svg('<path d="M5 12h13"/><path d="m12 5 7 7-7 7"/>'),
  "check":   svg('<path d="M20 6 9 17l-5-5"/>'),
  "eye":     svg('<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/>'
                 '<circle cx="12" cy="12" r="3"/>'),
  "eyeoff":  svg('<path d="M4 4l16 16"/>'
                 '<path d="M9.9 5.9A9.7 9.7 0 0 1 12 5.5c6 0 9.5 6.5 9.5 6.5a17 17 0 0 1-3.3 4"/>'
                 '<path d="M6.4 7.9A17 17 0 0 0 2.5 12S6 18.5 12 18.5a9.6 9.6 0 0 0 3.6-.7"/>'
                 '<path d="M9.9 10.2a3 3 0 0 0 4 4.2"/>'),
  "spark":   svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>'),
  "user":    svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>'),
  "users":   svg('<circle cx="9" cy="8" r="3.4"/><path d="M2.5 20c0-3.4 2.9-5.2 6.5-5.2s6.5 1.8 6.5 5.2"/><path d="M17 8.4a3 3 0 0 1 0 5.2M18.5 20c0-2.2-.8-3.7-2-4.6"/>'),
  "shield":  svg('<path d="M12 3 5 6v5.5c0 4.5 3 8 7 9.5 4-1.5 7-5 7-9.5V6l-7-3Z"/><path d="m9.2 12 2 2 3.6-3.8"/>'),
  "card":    svg('<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10h19"/>'),
  "bank":    svg('<path d="M3 10h18L12 4 3 10Z"/><path d="M5.5 10v7M10 10v7M14 10v7M18.5 10v7M3 20h18"/>'),
  "chart":   svg('<path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/>'),
  "globe":   svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.4 2.6 3.6 5.6 3.6 9s-1.2 6.4-3.6 9c-2.4-2.6-3.6-5.6-3.6-9S9.6 5.6 12 3Z"/>'),
  "clock":   svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.3 2"/>'),
  "code":    svg('<path d="m9 8-5 4 5 4M15 8l5 4-5 4"/>'),
  "lock":    svg('<rect x="4.5" y="10" width="15" height="10" rx="2.6"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>'),
  "phone":   svg('<path d="M6.5 3.5h3l1.6 4-2 1.4a12 12 0 0 0 6 6l1.4-2 4 1.6v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7 2 2 0 0 1 6.5 3.5Z"/>'),
  "mail":    svg('<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="m3.5 7 8.5 6 8.5-6"/>'),
  "pin":     svg('<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>'),
  "chat":    svg('<path d="M20 15a3 3 0 0 1-3 3H8l-4 3V6a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v9Z"/>'),
  "book":    svg('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20v3H6.5A2.5 2.5 0 0 1 4 20.5Z"/>'),
  "wave":    svg('<path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/><path d="M11 5 6.5 9H3v6h3.5L11 19V5Z"/>'),
  "star":    svg('<path d="m12 3 2.6 5.6 6.1.8-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L3.3 9.4l6.1-.8L12 3Z"/>', stroke=False),
  "plus":    svg('<path d="M12 5v14M5 12h14"/>'),
  "heart":   svg('<path d="M12 20s-7-4.4-7-9.2A4 4 0 0 1 12 8a4 4 0 0 1 7 2.8C19 15.6 12 20 12 20Z"/>'),
  "target":  svg('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>'),
  "layers":  svg('<path d="m12 3 8.5 4.5L12 12 3.5 7.5 12 3Z"/><path d="m3.5 12 8.5 4.5L20.5 12"/>'),
  "refresh": svg('<path d="M20 11a8 8 0 0 0-13.7-5.2L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 13.7 5.2L20 16"/><path d="M20 20v-4h-4"/>'),
  "x":       svg('<path d="M6 6l12 12M18 6 6 18"/>'),
  "in":      svg('<path d="M5 9v10M5 5.2v.1M10 19v-5.5a2.5 2.5 0 0 1 5 0V19M10 19v-9"/>'),
  "fb":      svg('<path d="M14.5 8.5H17V5h-2.5A4 4 0 0 0 10.5 9v2H8v3.5h2.5V22H14v-7.5h2.6l.4-3.5H14V9.5a1 1 0 0 1 .5-1Z"/>', stroke=False),
  "ig":      svg('<rect x="4" y="4" width="16" height="16" rx="4.6"/><circle cx="12" cy="12" r="3.4"/><path d="M16.8 7.3v.1"/>'),
}

# --------------------------------------------------------------------------
# Shared shell
# --------------------------------------------------------------------------
NAV = [
    ("Home", "index.html"),
    ("About", "about.html"),
    ("Benefits", "benefits.html"),
    ("Testimonials", "testimonials.html"),
    ("Career", "career.html"),
    ("Blog", "blog.html"),
    ("Support", "support.html"),
    ("Contact", "contact.html"),
]

BRAND = ('<a class="brand" href="index.html">'
         '<span class="brand__mark">%s</span>Finbolt</a>') % I["bolt"]


def nav_links(active, cls=""):
    out = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return "\n        ".join(out)


def header(active):
    return """  <header class="header">
    <div class="wrap header__inner">
      %s
      <nav class="nav" aria-label="Primary">
        %s
      </nav>
      <a class="header__login" href="login.html">Log in</a>
      <a class="header__cta" href="register.html">Get started<span class="dot">%s</span></a>
      <button class="burger" data-drawer-open aria-label="Open menu">
        <span class="burger__bars"><i></i><i></i><i></i></span>Menu
      </button>
    </div>
  </header>

  <div class="drawer" data-drawer data-open="false" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer__panel">
      <div class="drawer__head">
        %s
        <button class="drawer__close" data-drawer-close aria-label="Close menu">&times;</button>
      </div>
      <nav aria-label="Mobile">
        %s
      </nav>
      <a class="btn btn--primary" href="register.html">Get started%s</a>
      <a class="btn btn--ghost" href="login.html" style="width:100%%;justify-content:center;margin-top:10px">Log in</a>
    </div>
  </div>
""" % (BRAND, nav_links(active), I["arrow"], BRAND, nav_links(active), I["arrow"])


def cta_band(title, sub=""):
    return """  <section class="band cta">
    <div class="wrap cta__inner">
      <span class="eyebrow eyebrow--onblue"><i>%s</i>Finbolt payments, faster</span>
      <h2 style="margin-top:18px">%s</h2>
      %s
      <form class="capture" data-capture>
        <label class="sr-only" for="cta-email">Email address</label>
        <input id="cta-email" type="email" placeholder="Your email address" required>
        <button class="btn btn--dark" type="submit">Get started<span class="dot">%s</span></button>
      </form>
      <p class="capture__note">No card needed. Your first 30 days are free.</p>
    </div>
  </section>
""" % (I["bolt"], title,
       ('<p class="hero__sub">%s</p>' % sub) if sub else "",
       I["arrow"])


FOOTER = """  <footer class="footer">
    <div class="wrap footer__grid">
      <div>
        <p class="footer__blurb">Finbolt is built on one idea: getting paid should be the
          simplest part of running a business. We handle the plumbing so you can go
          back to the work you actually started the company to do.</p>
        %s
      </div>
      <div>
        <h4>Product</h4>
        <div class="footer__links">
          <a href="index.html">Home</a>
          <a href="benefits.html">Benefits</a>
          <a href="testimonials.html">Testimonials</a>
          <a href="support.html">Support centre</a>
          <a href="login.html">Log in</a>
          <a href="register.html">Create account</a>
        </div>
      </div>
      <div>
        <h4>Company</h4>
        <div class="footer__links">
          <a href="about.html">About</a>
          <a href="career.html">Career</a>
          <a href="blog.html">Blog</a>
          <a href="contact.html">Contact us</a>
        </div>
      </div>
      <div>
        <h4>Follow along</h4>
        <div class="social">
          <a href="#" aria-label="Finbolt on X">%s</a>
          <a href="#" aria-label="Finbolt on LinkedIn">%s</a>
          <a href="#" aria-label="Finbolt on Facebook">%s</a>
          <a href="#" aria-label="Finbolt on Instagram">%s</a>
        </div>
        <p class="footer__blurb" style="margin-top:16px">hello@finbolt.com<br>+234 700 346 6538</p>
      </div>
    </div>
    <div class="footer__bar">
      <span>Finbolt</span>
      <span>&copy; <span data-year>2026</span> Finbolt. All rights reserved.</span>
    </div>
  </footer>
""" % (BRAND.replace('class="brand"', 'class="brand"'), I["x"], I["in"], I["fb"], I["ig"])


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><text y='19' font-size='20'>&#9889;</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<div class="frame">
{header}
{main}
{footer}
</div>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def pagehead(title, sub, crumb):
    return """  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i>%s</i>%s</span>
      <h1 style="margin-top:18px">%s</h1>
      <p>%s</p>
      <p class="crumbs"><a href="index.html">Home</a> <span>/</span> <span>%s</span></p>
    </div>
  </section>
""" % (I["bolt"], crumb, title, sub, crumb)


def sechead(eyebrow, title, sub="", left=False):
    return """    <div class="sechead%s reveal">
      <span class="eyebrow"><i>%s</i>%s</span>
      <h2>%s</h2>
      %s
    </div>
""" % (" sechead--left" if left else "", I["bolt"], eyebrow, title,
       ('<p>%s</p>' % sub) if sub else "")


# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
PARTNERS = ["Northwind", "Lumeo", "Slatebox", "Orbitpay", "Fernway",
            "Kitewise", "Verolabs", "Maplehq"]

def logo_chips():
    chips = "".join(
        '<span class="logo-chip">%s%s</span>' % (I["bolt"], p) for p in PARTNERS)
    return chips + chips  # duplicated for the seamless marquee


AUDIENCES = [
    ("startups", I["spark"], "Start-ups",
     "Create and share professional invoices, then let Finbolt chase the reminders "
     "on recurring payments so you never have to.",
     "24K+", "Teams building on Finbolt"),
    ("freelancers", I["user"], "Freelancers",
     "Collect payments from clients anywhere in the world. Set up a business, "
     "start selling online and get paid the same day.",
     "61K+", "Independents paid worldwide"),
    ("enterprises", I["layers"], "Enterprises",
     "Route high volumes across entities and currencies, with approvals, audit "
     "trails and settlement reporting built in.",
     "820+", "Finance teams at scale"),
]

def audience_cards(live="freelancers"):
    out = []
    for key, icon, title, body, stat, statlabel in AUDIENCES:
        cls = "fcard reveal" + (" fcard--live" if key == live else "")
        out.append("""      <article class="%s" data-panel="%s">
        <span class="fcard__icon">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <div class="fcard__foot">
          <span class="fcard__stat"><b>%s</b> %s</span>
          <a class="btn btn--ghost" href="benefits.html">Learn more%s</a>
        </div>
      </article>""" % (cls, key, icon, title, body, stat, statlabel, I["arrow"]))
    return "\n".join(out)


HOME = """  <section class="band">
    <div class="wrap hero">
      <span class="eyebrow eyebrow--onblue"><i>%(bolt)s</i>Finbolt payments, faster</span>
      <h1 style="margin-top:20px">Make your business payment fast
        and secure, with <span class="inline-mark">%(bolt)s</span>Finbolt</h1>
      <p class="hero__sub">One account for invoices, cards, transfers and payouts —
        live in four minutes, with money in your bank the same day.</p>
      <form class="capture" data-capture>
        <label class="sr-only" for="hero-email">Email address</label>
        <input id="hero-email" type="email" placeholder="Your email address" required>
        <button class="btn btn--dark" type="submit">Get started<span class="dot">%(arrow)s</span></button>
      </form>
      <p class="capture__note">Free for 30 days. No card needed.</p>

      <div class="hero__stage">
        <div class="stage-col">
          <div class="mock">
            <div class="metric">
              <span class="mock__row"><span class="avatar avatar--sm">%(boltsm)s</span>
                <b class="metric__value">+10k</b></span>
              <span class="pill-tag pill-tag--green">Live</span>
            </div>
          </div>
          <div class="mock">
            <p class="mock__label" style="margin:0">Your current plan</p>
            <div class="metric" style="margin-top:4px">
              <b class="metric__value" style="font-size:1.05rem">Developer</b>
              <span class="plan__price">$99<sub>/mo</sub></span>
            </div>
            <div class="plan__feat">
              <span>%(users)s 5 users</span>
              <span>%(shield)s Dedicated support</span>
            </div>
          </div>
        </div>

        <div class="stage-col stage-col--center">
          <div class="mock">
            <div class="mock__row">
              <span class="avatar">%(card)s</span>
              <span>
                <span class="mock__label">Payments</span>
                <b style="display:block;font-family:var(--font-display)">Finbolt payment</b>
              </span>
            </div>
            <p class="mock__amount" style="margin:14px 0 0">$3,050.00<sub>USD</sub></p>
            <span class="pill-tag pill-tag--green" style="margin-top:6px">Cleared</span>
            <p class="mock__label" style="margin:16px 0 0;font-weight:600;color:var(--ink)">Payment method</p>
            <div class="cardface">
              <div style="display:flex;align-items:center;justify-content:space-between">
                <span class="cardface__chip"></span>
                <span style="color:var(--blue);width:18px">%(wave)s</span>
              </div>
              <p class="cardface__num">3455 4562 7710 3507</p>
              <p class="cardface__meta"><span>John Carter</span><span>02/30</span></p>
            </div>
          </div>
        </div>

        <div class="stage-col">
          <div class="mock">
            <div class="mock__row">
              <span class="avatar">JC</span>
              <span>
                <span class="mock__label">Total balance</span>
                <b style="display:block;font-family:var(--font-display)">John Clayton</b>
              </span>
            </div>
          </div>
          <div class="mock">
            <p class="mock__label" style="margin:0">This month</p>
            <p class="mock__amount" style="margin:4px 0 0">$3,050.00<sub>USD</sub></p>
            <div class="balance__split">
              <div class="balance__cell">
                <span class="mock__label">Income</span>
                <b>$1,400.21</b>
              </div>
              <div class="balance__cell">
                <span class="mock__label">Expenses</span>
                <b>$40.00</b>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="trusted">
    <div class="wrap reveal">
      <h2>Trusted by more than <em>+10,000</em> businesses</h2>
    </div>
    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">%(chips)s</div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(head1)s
      <div class="tabs reveal" role="tablist" aria-label="Who Finbolt is for">
        <button class="tab" role="tab" data-tab="startups" aria-selected="false"><i>%(spark)s</i>Start-ups</button>
        <button class="tab" role="tab" data-tab="freelancers" aria-selected="true"><i>%(user)s</i>Freelancers</button>
        <button class="tab" role="tab" data-tab="enterprises" aria-selected="false"><i>%(layers)s</i>Enterprises</button>
      </div>
      <div class="grid grid--3">
%(cards)s
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
%(head2)s
      <div class="showcase reveal">
        <div class="showcase__glow"></div>
        <div class="invoice">
          <div class="invoice__top">
            <span class="avatar">%(boltsm)s</span>
            <span>
              <b style="font-family:var(--font-display);color:var(--ink)">Invoice from Finbolt</b>
              <span class="mock__label" style="display:block">Billed to John Clayton</span>
            </span>
            <span class="invoice__amount">
              <b>$350.00</b>
              <span>Due Aug 9, 2026</span>
            </span>
          </div>
          <div class="invoice__grid">
            <span class="field">%(card)s Card</span>
            <span class="field">%(bank)s Bank transfer</span>
          </div>
          <div class="invoice__grid" style="grid-template-columns:1.6fr 1fr">
            <span class="field">%(lock)s Card number</span>
            <span class="field field--split">
              <span class="field">MM / YY</span>
              <span class="field">CVC</span>
            </span>
          </div>
          <a class="btn btn--primary" href="support.html">Pay invoice%(arrow)s</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(head3)s
      <div class="constellation reveal">
        <div class="constellation__side">
          <span class="person"><span class="avatar avatar--sm">AM</span>
            <span class="pill-tag pill-tag--green">+$40.00</span></span>
          <span class="person"><span class="avatar avatar--sm">TO</span>
            <span class="pill-tag pill-tag--rose">-$40.00</span></span>
        </div>
        <div>
          <div class="mock" style="box-shadow:var(--shadow-md), inset 0 0 0 1px var(--line);background:#fff">
            <div class="mock__row">
              <span class="avatar">JC</span>
              <span>
                <span class="mock__label">Total balance</span>
                <b style="display:block;font-family:var(--font-display)">John Clayton</b>
              </span>
            </div>
          </div>
          <div class="balance" style="margin-top:14px">
            <p class="mock__amount" style="margin:0">$3,050.00<sub>USD</sub></p>
            <div class="balance__split">
              <div class="balance__cell"><span class="mock__label">Income</span><b>$1,400.21</b></div>
              <div class="balance__cell"><span class="mock__label">Expenses</span><b>$40.00</b></div>
            </div>
          </div>
        </div>
        <div class="constellation__side constellation__side--right">
          <span class="person"><span class="avatar avatar--sm">KE</span>
            <span class="pill-tag pill-tag--rose">-$40.00</span></span>
          <span class="person"><span class="avatar avatar--sm">BN</span>
            <span class="pill-tag pill-tag--green">+$40.00</span></span>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div>
%(head4)s
        <ul class="split__list">
          <li><i>%(target)s</i>Optimise payments</li>
          <li><i>%(chart)s</i>Grow your revenue</li>
          <li><i>%(globe)s</i>Work on the go</li>
          <li><i>%(shield)s</i>Put security first</li>
        </ul>
        <a class="btn btn--primary" href="benefits.html" style="margin-top:26px">See every benefit%(arrow)s</a>
      </div>
      <div class="paystack reveal">
        <div class="mock" style="background:#fff;box-shadow:var(--shadow-md), inset 0 0 0 1px var(--line)">
          <div class="mock__row">
            <span class="avatar">%(card)s</span>
            <span>
              <span class="mock__label">Payments</span>
              <b style="display:block;font-family:var(--font-display)">Finbolt payment</b>
            </span>
          </div>
          <p class="mock__amount" style="margin:14px 0 0">$3,050.00<sub>USD</sub></p>
          <span class="pill-tag pill-tag--green" style="margin-top:6px">Cleared</span>
          <p class="mock__label" style="margin:16px 0 0;font-weight:600;color:var(--ink)">Payment method</p>
          <div class="cardface">
            <div style="display:flex;align-items:center;justify-content:space-between">
              <span class="cardface__chip"></span>
              <span style="color:var(--blue);width:18px">%(wave)s</span>
            </div>
            <p class="cardface__num">3455 4562 7710 3507</p>
            <p class="cardface__meta"><span>John Carter</span><span>02/30</span></p>
          </div>
        </div>
        <div class="notice"><i>%(check)s</i>Payment successful</div>
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "bolt": I["bolt"], "boltsm": I["bolt"], "arrow": I["arrow"], "check": I["check"],
    "users": I["users"], "shield": I["shield"], "card": I["card"], "bank": I["bank"],
    "lock": I["lock"], "wave": I["wave"], "spark": I["spark"], "user": I["user"],
    "layers": I["layers"], "target": I["target"], "chart": I["chart"], "globe": I["globe"],
    "chips": logo_chips(),
    "cards": audience_cards(),
    "head1": sechead("Finbolt, easy to use",
                     "Get the most powerful and <em>easy to use</em> payment software",
                     "Pick the setup that matches how you work today — you can change it "
                     "any time without moving your money."),
    "head2": sechead("Finbolt payments, faster",
                     "Rewards that are endlessly <em>rewarding</em> for every transaction",
                     "Earn scratch cards and rewards on every payment, send them straight "
                     "to your bank account, and get a nudge before a coupon expires."),
    "head3": sechead("Finbolt payments, secure",
                     "Keep your money secure <em>always</em>",
                     "Finbolt watches every transaction for fraud and blocks the ones that "
                     "look wrong. Lock the app behind your face or fingerprint in one tap."),
    "head4": sechead("Finbolt payments, speed",
                     "Collect all payments within <em>minutes</em>",
                     "Drop Finbolt into your site or app with our APIs and plugins. "
                     "Your customers pay however they want to pay.", left=True),
    "cta": cta_band("Start accepting payments in just 4 minutes"),
}

# --------------------------------------------------------------------------
# ABOUT
# --------------------------------------------------------------------------
VALUES = [
    (I["shield"], "Money first, features second",
     "Every release is judged on one question: does it make settlement safer or faster? "
     "If it does neither, it waits."),
    (I["globe"], "Built for the market we're in",
     "Local rails, local currencies, local support hours. We started in Lagos and we "
     "build for the businesses around us."),
    (I["chat"], "Answer, then fix",
     "Support replies in minutes and the engineer who wrote the code sees the ticket. "
     "Nobody hides behind a queue."),
    (I["target"], "Boring where it counts",
     "Payments should be the least dramatic part of your week. We keep the excitement "
     "for the product, not the ledger."),
]

TIMELINE = [
    ("2021", "Two people and a spreadsheet",
     "Finbolt started as an internal tool for reconciling client payments at a small "
     "agency. It reconciled in seconds what took a full day by hand."),
    ("2022", "First 500 businesses",
     "We opened it up, added card and transfer collection, and hit five hundred paying "
     "businesses before we had a marketing page."),
    ("2024", "Multi-currency payouts",
     "Freelancers asked to be paid across borders without losing a cut to intermediaries. "
     "We built settlement in eleven currencies."),
    ("2026", "10,000 businesses",
     "Finbolt now moves money for more than ten thousand businesses, from one-person "
     "studios to finance teams running several entities."),
]

ABOUT = """%(head)s
  <section class="section">
    <div class="wrap split">
      <div>
%(sec)s
        <p>Getting paid used to mean chasing invoices, reconciling three different
          dashboards and explaining to a client why the transfer had not landed yet.
          We had done all of that ourselves, badly, for years.</p>
        <p>So Finbolt was built the other way round: start from the moment money is
          owed, and remove every step between that moment and the money sitting in
          your account. Invoices that send themselves. Payments that reconcile
          automatically. Payouts that arrive the same day.</p>
        <p>We are a team of forty across Lagos, Nairobi and Berlin, and we are still
          building toward the same thing — a business owner who never has to think
          about payments again.</p>
        <a class="btn btn--primary" href="career.html" style="margin-top:12px">Work with us%(arrow)s</a>
      </div>
      <div class="reveal">
        <div class="stats stats--2">
          <div class="stat"><b>10,400+</b><span>Businesses paid</span></div>
          <div class="stat"><b>$2.1B</b><span>Processed in 2025</span></div>
          <div class="stat"><b>11</b><span>Settlement currencies</span></div>
          <div class="stat"><b>99.98%%</b><span>Uptime last 12 months</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(vhead)s
      <div class="grid grid--2">
%(values)s
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
%(thead)s
      <div class="timeline reveal">
%(timeline)s
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("A payments company that started as a spreadsheet",
                     "Finbolt exists because we were tired of chasing our own invoices. "
                     "Here is where the company came from and what we are building next.",
                     "About"),
    "sec": sechead("Our story", "Why we built <em>Finbolt</em>", left=True),
    "vhead": sechead("What we believe", "Four things we won't <em>trade away</em>"),
    "thead": sechead("Our path", "How Finbolt <em>grew up</em>"),
    "values": "\n".join(
        """      <article class="fcard reveal">
        <span class="fcard__icon">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </article>""" % (icon, t, b) for icon, t, b in VALUES),
    "timeline": "\n".join(
        """        <div class="tl">
          <b>%s</b>
          <div><h3>%s</h3><p>%s</p></div>
        </div>""" % (y, t, b) for y, t, b in TIMELINE),
    "arrow": I["arrow"],
    "cta": cta_band("Come build the boring, brilliant parts of money"),
}

# --------------------------------------------------------------------------
# BENEFITS
# --------------------------------------------------------------------------
BENEFITS = [
    (I["clock"], "Same-day settlement",
     "Money collected before 6pm lands in your bank the same day, not in three "
     "working days. Weekends included."),
    (I["card"], "Every payment method",
     "Cards, bank transfers, USSD, wallets and direct debit — one integration, "
     "one dashboard, one reconciliation."),
    (I["globe"], "Eleven currencies",
     "Invoice a client in their currency and settle in yours, at the mid-market "
     "rate with the fee shown up front."),
    (I["shield"], "Fraud screening on by default",
     "Every transaction is scored before it clears. Suspicious ones are held for "
     "review instead of quietly going through."),
    (I["refresh"], "Recurring billing",
     "Set a schedule once. Finbolt raises the invoice, takes the payment and "
     "sends the receipt without being asked."),
    (I["code"], "APIs your developers will like",
     "Predictable REST endpoints, signed webhooks, and SDKs for Node, Python, PHP "
     "and Go. Test keys work instantly."),
]

PLANS = [
    ("Starter", "$0", "/mo",
     ["1.4% + $0.20 per transaction", "Unlimited invoices", "Same-day settlement",
      "Email support"], False),
    ("Developer", "$99", "/mo",
     ["1.1% + $0.15 per transaction", "5 team members", "Full API and webhooks",
      "Dedicated support", "Sandbox environments"], True),
    ("Scale", "Custom", "",
     ["Volume pricing", "Unlimited team members", "Multi-entity routing",
      "Named account manager", "99.99% uptime SLA"], False),
]

def plan_cards():
    out = []
    for name, price, per, feats, live in PLANS:
        cls = "fcard reveal" + (" fcard--live" if live else "")
        items = "".join('<li style="display:flex;gap:9px;align-items:flex-start;margin-top:9px;font-size:.9rem">'
                        '<span style="width:15px;flex:none;margin-top:3px">%s</span>%s</li>' % (I["check"], f)
                        for f in feats)
        out.append("""      <article class="%s">
        <h3>%s</h3>
        <p style="margin:0"><span class="plan__price" style="font-size:2rem">%s</span>
          <span style="font-size:.8rem;color:var(--muted)">%s</span></p>
        <ul style="margin:6px 0 0">%s</ul>
        <div class="fcard__foot">
          <a class="btn %s" href="contact.html" style="width:100%%;justify-content:center">Choose %s%s</a>
        </div>
      </article>""" % (cls, name, price, per, items,
                       "btn--ghost" if live else "btn--primary", name, I["arrow"]))
    return "\n".join(out)


BENEFITS_PAGE = """%(head)s
  <section class="section">
    <div class="wrap">
%(bhead)s
      <div class="grid grid--3">
%(cards)s
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap split">
      <div>
%(shead)s
        <p>Finbolt does not hold your settlement to improve its own float. Money is
          swept to your account on the schedule you choose, and the fee is the same
          number you saw when you signed up.</p>
        <ul class="split__list">
          <li><i>%(check)s</i>No monthly minimum</li>
          <li><i>%(check)s</i>No setup fee</li>
          <li><i>%(check)s</i>No charge for failed payments</li>
          <li><i>%(check)s</i>Cancel any time</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="invoice">
          <div class="invoice__top">
            <span class="avatar">%(chart)s</span>
            <span>
              <b style="font-family:var(--font-display);color:var(--ink)">Settlement summary</b>
              <span class="mock__label" style="display:block">August 2026</span>
            </span>
          </div>
          <div class="balance__split" style="margin-top:18px">
            <div class="balance__cell"><span class="mock__label">Collected</span><b>$48,210.00</b></div>
            <div class="balance__cell"><span class="mock__label">Finbolt fee</span><b>$530.31</b></div>
          </div>
          <div class="balance__cell" style="margin-top:10px">
            <span class="mock__label">Paid to your bank</span>
            <b style="font-size:1.3rem">$47,679.69</b>
          </div>
          <div class="notice" style="margin-top:14px"><i>%(check)s</i>Settled same day, 6:04pm</div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
%(phead)s
      <div class="grid grid--3">
%(plans)s
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("Everything you get with Finbolt",
                     "The features that matter when money is moving — and the pricing "
                     "that goes with them, written out in full.",
                     "Benefits"),
    "bhead": sechead("Finbolt benefits", "Built for the way money <em>actually moves</em>"),
    "shead": sechead("Fair pricing", "One rate, shown <em>up front</em>", left=True),
    "phead": sechead("Plans", "Pick a plan, change it <em>whenever</em>",
                     "Every plan includes same-day settlement, fraud screening and the full API."),
    "cards": "\n".join(
        """      <article class="fcard reveal">
        <span class="fcard__icon">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </article>""" % (icon, t, b) for icon, t, b in BENEFITS),
    "plans": plan_cards(),
    "check": I["check"], "chart": I["chart"],
    "cta": cta_band("Start collecting on the fair rate today"),
}

# --------------------------------------------------------------------------
# TESTIMONIALS
# --------------------------------------------------------------------------
QUOTES = [
    ("We moved 1,800 subscriptions to Finbolt over a weekend and not one customer "
     "noticed. That is the highest compliment I can pay a payments provider.",
     "Amara Eze", "Finance lead, Northwind Studios", "AE"),
    ("I invoice clients in four countries. Before Finbolt I lost about 6% of every "
     "invoice to conversion and intermediary fees. Now I see the rate before I send it.",
     "Tunde Olawale", "Independent product designer", "TO"),
    ("The fraud screening caught a card-testing run at 2am and held 40 transactions. "
     "We would have found out from the chargebacks three weeks later.",
     "Grace Mensah", "Head of ops, Lumeo", "GM"),
    ("Their support answered in nine minutes on a Sunday, and the person replying had "
     "actually read the webhook logs. Rare.",
     "Daniel Okonkwo", "CTO, Kitewise", "DO"),
    ("Same-day settlement changed how we buy stock. We are no longer financing three "
     "days of somebody else's float.",
     "Blessing Nwosu", "Owner, Fernway Foods", "BN"),
    ("The API took an afternoon. The sandbox behaves exactly like production, which is "
     "not something I can say about the last three providers.",
     "Kelechi Anyanwu", "Engineer, Slatebox", "KA"),
]

def quote_cards():
    stars = '<span class="stars">%s</span>' % (I["star"] * 5)
    return "\n".join(
        """      <article class="quote reveal">
        %s
        <p>%s</p>
        <div class="quote__who">
          <span class="avatar">%s</span>
          <span><b>%s</b><span>%s</span></span>
        </div>
      </article>""" % (stars, q, ini, name, role)
        for q, name, role, ini in QUOTES)


TESTIMONIALS_PAGE = """%(head)s
  <section class="section">
    <div class="wrap">
%(fhead)s
      <div class="grid grid--2 reveal" style="align-items:stretch">
        <article class="quote quote--feature">
          <span class="stars" style="color:#fff">%(stars)s</span>
          <p>&ldquo;We switched to Finbolt to stop chasing payments. Six months later
            our days-sales-outstanding went from 34 days to 9, and I have not sent a
            single reminder email myself.&rdquo;</p>
          <div class="quote__who">
            <span class="avatar" style="background:rgba(6,26,70,.38)">JC</span>
            <span><b>John Clayton</b><span>Managing director, Orbitpay</span></span>
          </div>
        </article>
        <div class="stats stats--2">
          <div class="stat"><b>4.9/5</b><span>Average review score</span></div>
          <div class="stat"><b>10,400+</b><span>Businesses on Finbolt</span></div>
          <div class="stat"><b>9 min</b><span>Median support reply</span></div>
          <div class="stat"><b>96%%</b><span>Would recommend us</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(ghead)s
      <div class="grid grid--3">
%(quotes)s
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("What businesses say about Finbolt",
                     "Reviews from the people who send the invoices, reconcile the "
                     "statements and answer to the board.",
                     "Testimonials"),
    "fhead": sechead("Customer stories", "Rated <em>4.9 out of 5</em> by 2,300 businesses"),
    "ghead": sechead("In their words", "Six teams, six <em>different problems</em>"),
    "stars": I["star"] * 5,
    "quotes": quote_cards(),
    "cta": cta_band("Join 10,000 businesses that stopped chasing invoices"),
}

# --------------------------------------------------------------------------
# CAREER
# --------------------------------------------------------------------------
ROLES = [
    ("Senior backend engineer (payments core)", ["Lagos or remote", "Full time", "Engineering"]),
    ("Product designer", ["Remote (WAT ±3)", "Full time", "Design"]),
    ("Compliance analyst", ["Lagos", "Full time", "Risk & compliance"]),
    ("Support engineer, weekend cover", ["Remote", "Part time", "Support"]),
    ("Partnerships manager, East Africa", ["Nairobi", "Full time", "Growth"]),
    ("Technical writer", ["Remote", "Contract", "Documentation"]),
]

PERKS = [
    (I["heart"], "Private health cover", "Full cover for you, a partner and up to three dependants, from day one."),
    (I["globe"], "Remote by default", "Work where you work best. We meet in person twice a year, company-paid."),
    (I["book"], "Learning budget", "$2,000 a year for courses, conferences and books — no approval chain."),
    (I["clock"], "Real time off", "28 days, and the founders check that you actually take them."),
]

CAREER_PAGE = """%(head)s
  <section class="section">
    <div class="wrap split">
      <div>
%(whead)s
        <p>Payments is a field where a small mistake is somebody's payroll. That makes
          the work slower and more careful than most software jobs, and it makes it
          matter more.</p>
        <p>We hire people who want to own a problem end to end — writing the code,
          watching it in production, and reading the support tickets it generates. No
          throwing work over a wall.</p>
        <ul class="split__list">
          <li><i>%(check)s</i>Salary bands published internally</li>
          <li><i>%(check)s</i>Four-stage interview, two weeks</li>
          <li><i>%(check)s</i>Paid take-home task</li>
          <li><i>%(check)s</i>Feedback either way</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="stats stats--2">
          <div class="stat"><b>41</b><span>People on the team</span></div>
          <div class="stat"><b>9</b><span>Countries</span></div>
          <div class="stat"><b>3.1 yrs</b><span>Median tenure</span></div>
          <div class="stat"><b>6</b><span>Roles open now</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(rhead)s
      <div class="grid" style="gap:14px">
%(roles)s
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
%(phead)s
      <div class="grid grid--4">
%(perks)s
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("Build the rails, not just the app",
                     "We are forty-one people across nine countries, moving money for "
                     "ten thousand businesses. Six roles are open right now.",
                     "Career"),
    "whead": sechead("Why Finbolt", "Careful work, on <em>things that matter</em>", left=True),
    "rhead": sechead("Open roles", "Six roles, <em>hiring now</em>",
                     "Do not see your role? Send us a note anyway — we read every one."),
    "phead": sechead("Perks", "What we <em>actually offer</em>"),
    "roles": "\n".join(
        """      <article class="row-card reveal">
        <div>
          <h3>%s</h3>
          <div class="row-card__meta">%s</div>
        </div>
        <a class="btn btn--primary" href="contact.html">Apply%s</a>
      </article>""" % (title, "".join("<span>%s</span>" % m for m in meta), I["arrow"])
        for title, meta in ROLES),
    "perks": "\n".join(
        """      <article class="fcard reveal">
        <span class="fcard__icon">%s</span>
        <h3 style="font-size:1.02rem">%s</h3>
        <p>%s</p>
      </article>""" % (icon, t, b) for icon, t, b in PERKS),
    "check": I["check"],
    "cta": cta_band("Think you'd fit? We'd like to hear from you"),
}

# --------------------------------------------------------------------------
# BLOG
# --------------------------------------------------------------------------
POSTS = [
    ("Why we settle the same day, even though float is profitable",
     "Holding your money for three days would earn us real money. Here is the "
     "arithmetic, and why we decided against it anyway.",
     "Product", "6 min read", I["clock"]),
    ("A field guide to card-testing attacks",
     "What a card-testing run looks like in your logs, why it usually happens at 2am, "
     "and the three signals that catch it early.",
     "Security", "9 min read", I["shield"]),
    ("Multi-currency invoicing without losing 6% to fees",
     "Where the money actually goes when you invoice across borders, and how to "
     "structure an invoice so the client pays the conversion.",
     "Guides", "7 min read", I["globe"]),
    ("Designing a payment form people finish",
     "We tested eleven versions of one checkout form. The winner had fewer fields and "
     "one very unglamorous change to the error copy.",
     "Design", "5 min read", I["target"]),
    ("Webhooks that survive your outage",
     "Idempotency keys, replay windows and the retry schedule we settled on after "
     "getting it wrong twice.",
     "Engineering", "11 min read", I["code"]),
    ("Reconciliation for people who hate reconciliation",
     "A short, practical routine for closing your month in under an hour, whether or "
     "not you use Finbolt.",
     "Guides", "4 min read", I["chart"]),
]

BLOG_PAGE = """%(head)s
  <section class="section">
    <div class="wrap">
%(fhead)s
      <article class="split reveal" style="gap:34px;align-items:center">
        <div class="post__thumb" style="border-radius:var(--r-lg);aspect-ratio:4/3">%(chart)s</div>
        <div>
          <span class="pill-tag" style="background:var(--blue-tint);color:var(--blue-deep)">Product</span>
          <h3 style="font-size:var(--fs-h3);margin:14px 0 10px">The 2026 state of getting paid in West Africa</h3>
          <p style="color:var(--muted);font-size:.95rem">We looked at 4.1 million transactions across
            ten thousand Finbolt businesses to answer one question: how long does it actually
            take a small business to get paid, and what makes the difference? The gap between
            the fastest and slowest quartile is 27 days — and almost none of it is about the client.</p>
          <p class="post__meta" style="padding-top:14px">August 12, 2026 &middot; 14 min read</p>
          <a class="btn btn--primary" href="#" style="margin-top:6px">Read the report%(arrow)s</a>
        </div>
      </article>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(lhead)s
      <div class="grid grid--3">
%(posts)s
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("Notes on money, fraud and getting paid",
                     "What we learn running payments for ten thousand businesses, written "
                     "up for the people doing the same job.",
                     "Blog"),
    "fhead": sechead("Featured", "This month's <em>long read</em>"),
    "lhead": sechead("All posts", "From the <em>Finbolt team</em>"),
    "posts": "\n".join(
        """      <article class="post reveal">
        <div class="post__thumb">%s</div>
        <div class="post__body">
          <h3>%s</h3>
          <p>%s</p>
          <div class="post__meta">
            <span class="pill-tag">%s</span><span>%s</span>
          </div>
        </div>
      </article>""" % (icon, t, b, tag, read) for t, b, tag, read, icon in POSTS),
    "chart": I["chart"], "arrow": I["arrow"],
    "cta": cta_band("Get the next post before anyone else"),
}

# --------------------------------------------------------------------------
# SUPPORT
# --------------------------------------------------------------------------
SUPPORT_CATS = [
    (I["spark"], "Getting started", "Open an account, verify your business and take your first payment."),
    (I["card"], "Payments and payouts", "Settlement times, failed charges, refunds and chargebacks."),
    (I["code"], "Developers", "API reference, webhooks, SDKs, test keys and sandbox behaviour."),
    (I["shield"], "Security and compliance", "Two-factor, device locks, KYC documents and data requests."),
    (I["chart"], "Billing and plans", "Invoices from Finbolt, changing plan, and how fees are calculated."),
    (I["users"], "Team and access", "Adding people, roles, approval limits and audit logs."),
]

FAQS = [
    ("How long does verification take?",
     "Most businesses are verified within two hours during working days. If we need a "
     "document you have not uploaded, you will get an email naming exactly which one."),
    ("When does money reach my bank account?",
     "Payments collected before 6pm settle the same day, including weekends. Anything "
     "after 6pm settles the next morning. You can also set a weekly sweep instead."),
    ("What happens if a payment is flagged for fraud?",
     "It is held rather than declined, and you get a notification with the reason. You "
     "can release or reject it from the dashboard, and the customer is not charged until you do."),
    ("Can I use Finbolt without writing any code?",
     "Yes. Invoices, payment links and the checkout page all work from the dashboard. "
     "The API is there when you want to automate, not a requirement."),
    ("How do refunds work?",
     "Full or partial refunds are issued from the transaction page and reach the customer "
     "in three to five days depending on their bank. We do not charge a fee to refund."),
    ("Is there a limit on transaction size?",
     "Starter accounts are capped at $10,000 per transaction until the first month closes. "
     "After that, limits are set with your account manager based on your volume."),
]

SUPPORT_PAGE = """%(head)s
  <section class="section">
    <div class="wrap">
%(chead)s
      <div class="grid grid--3">
%(cats)s
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(fhead)s
      <div class="acc reveal">
%(faqs)s
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
%(hhead)s
      <div class="grid grid--3">
        <article class="fcard reveal">
          <span class="fcard__icon">%(chat)s</span>
          <h3>Live chat</h3>
          <p>The fastest route. Median reply is nine minutes, and the person answering
            can see your account.</p>
          <div class="fcard__foot"><a class="btn btn--primary" href="contact.html">Start a chat%(arrow)s</a></div>
        </article>
        <article class="fcard reveal">
          <span class="fcard__icon">%(mail)s</span>
          <h3>Email</h3>
          <p>Best for anything with attachments — documents, statements or screenshots
            of an error.</p>
          <div class="fcard__foot"><a class="btn btn--ghost" href="contact.html">help@finbolt.com%(arrow)s</a></div>
        </article>
        <article class="fcard reveal">
          <span class="fcard__icon">%(phone)s</span>
          <h3>Phone</h3>
          <p>For urgent settlement or suspected fraud. Open 8am to 8pm WAT, every day
            of the week.</p>
          <div class="fcard__foot"><a class="btn btn--ghost" href="contact.html">+234 700 346 6538%(arrow)s</a></div>
        </article>
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("Support centre",
                     "Answers to the questions we get most, and three ways to reach a "
                     "person if the answer isn't here.",
                     "Support"),
    "chead": sechead("Browse", "Find it by <em>topic</em>"),
    "fhead": sechead("Common questions", "Answered <em>properly</em>"),
    "hhead": sechead("Talk to us", "Reach a <em>real person</em>"),
    "cats": "\n".join(
        """      <article class="fcard reveal">
        <span class="fcard__icon">%s</span>
        <h3 style="font-size:1.05rem">%s</h3>
        <p>%s</p>
        <div class="fcard__foot"><span class="fcard__stat"><b>Browse articles</b></span>
          <span style="width:16px;color:var(--blue)">%s</span></div>
      </article>""" % (icon, t, b, I["arrow"]) for icon, t, b in SUPPORT_CATS),
    "faqs": "\n".join(
        """        <div class="acc__item" data-open="%s">
          <button class="acc__q" aria-expanded="%s"><span>%s</span><i>+</i></button>
          <div class="acc__a">%s</div>
        </div>""" % ("true" if i == 0 else "false", "true" if i == 0 else "false", q, a)
        for i, (q, a) in enumerate(FAQS)),
    "chat": I["chat"], "mail": I["mail"], "phone": I["phone"], "arrow": I["arrow"],
    "cta": cta_band("Still stuck? We'll get you moving"),
}

# --------------------------------------------------------------------------
# CONTACT
# --------------------------------------------------------------------------
CONTACT_PAGE = """%(head)s
  <section class="section">
    <div class="wrap split" style="gap:44px;align-items:start">
      <div>
%(fhead)s
        <form class="form" data-demo-form novalidate>
          <div class="form__ok">%(check)s Thanks — we've got your message and will reply within one working day.</div>
          <div class="form__row">
            <div><label for="c-first">First name</label><input id="c-first" type="text" placeholder="John" required></div>
            <div><label for="c-last">Last name</label><input id="c-last" type="text" placeholder="Clayton" required></div>
          </div>
          <div class="form__row">
            <div><label for="c-email">Work email</label><input id="c-email" type="email" placeholder="john@company.com" required></div>
            <div><label for="c-phone">Phone</label><input id="c-phone" type="tel" placeholder="+234 800 000 0000"></div>
          </div>
          <div>
            <label for="c-topic">What is this about?</label>
            <select id="c-topic">
              <option>Opening an account</option>
              <option>Pricing for my volume</option>
              <option>A problem with a payment</option>
              <option>Press or partnerships</option>
              <option>Something else</option>
            </select>
          </div>
          <div>
            <label for="c-msg">Message</label>
            <textarea id="c-msg" placeholder="Tell us what you need and roughly how much you process each month." required></textarea>
          </div>
          <button class="btn btn--primary" type="submit" style="justify-content:center">Send message%(arrow)s</button>
          <p class="form__note">This demo form does not send anywhere — connect it to your own
            backend or form service before going live.</p>
        </form>
      </div>

      <div class="reveal" style="display:grid;gap:14px">
        <article class="fcard">
          <span class="fcard__icon">%(chat)s</span>
          <h3 style="font-size:1.02rem">Talk to sales</h3>
          <p>If you process more than $50,000 a month, we will price it properly. Expect
            a reply the same working day.</p>
        </article>
        <article class="fcard">
          <span class="fcard__icon">%(mail)s</span>
          <h3 style="font-size:1.02rem">Email us</h3>
          <p>hello@finbolt.com for general questions.<br>help@finbolt.com if a payment
            needs attention.</p>
        </article>
        <article class="fcard">
          <span class="fcard__icon">%(pin)s</span>
          <h3 style="font-size:1.02rem">Where we are</h3>
          <p>14 Adeola Odeku Street, Victoria Island, Lagos<br>
            Westlands Square, Nairobi<br>
            Torstra&szlig;e 21, Berlin</p>
        </article>
        <article class="fcard">
          <span class="fcard__icon">%(clock)s</span>
          <h3 style="font-size:1.02rem">Hours</h3>
          <p>Support is open 8am&ndash;8pm WAT, seven days a week. Sales replies Monday
            to Friday.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="wrap">
%(qhead)s
      <div class="acc reveal">
        <div class="acc__item" data-open="true">
          <button class="acc__q" aria-expanded="true"><span>How quickly will someone reply?</span><i>+</i></button>
          <div class="acc__a">Support answers in about nine minutes on average during opening
            hours. Sales enquiries get a reply the same working day.</div>
        </div>
        <div class="acc__item" data-open="false">
          <button class="acc__q" aria-expanded="false"><span>Can I get a demo before I sign up?</span><i>+</i></button>
          <div class="acc__a">Yes — pick &ldquo;Opening an account&rdquo; above and mention a demo.
            It runs about 30 minutes on your own use case, not a slide deck.</div>
        </div>
        <div class="acc__item" data-open="false">
          <button class="acc__q" aria-expanded="false"><span>Do you work with businesses outside Africa?</span><i>+</i></button>
          <div class="acc__a">We settle in eleven currencies and support businesses registered
            in 34 countries. Tell us where you are incorporated and we will confirm.</div>
        </div>
      </div>
    </div>
  </section>

%(cta)s
""" % {
    "head": pagehead("Let's talk about your payments",
                     "Whether you are opening an account, comparing rates or chasing a "
                     "single transaction — this reaches the right desk.",
                     "Contact"),
    "fhead": sechead("Send a message", "Tell us what you <em>need</em>", left=True),
    "qhead": sechead("Before you write", "Quick <em>answers</em>"),
    "check": I["check"], "arrow": I["arrow"], "chat": I["chat"],
    "mail": I["mail"], "pin": I["pin"], "clock": I["clock"],
    "cta": cta_band("Or skip the form and open an account now"),
}

# --------------------------------------------------------------------------
# AUTH (login / register)
# --------------------------------------------------------------------------
AUTH_POINTS = {
    "login": [
        "Every account, card and payout on one dashboard",
        "Same-day settlement, seven days a week",
        "Fraud screening running on every transaction",
    ],
    "register": [
        "Live in about four minutes, no paperwork to post",
        "Free for 30 days &mdash; no card needed to start",
        "Keep your first $10,000 of payments fee-free",
    ],
}


def auth_pitch(mode):
    title = ("Welcome back to <em>Finbolt</em>" if mode == "login"
             else "Start getting paid <em>properly</em>")
    lead = ("Sign in to see today's settlements, chase an invoice or move money out."
            if mode == "login" else
            "Open an account, connect your first payment method and send an invoice "
            "before your coffee goes cold.")
    items = "\n        ".join(
        '<li>%s%s</li>' % (I["check"], t) for t in AUTH_POINTS[mode])
    return """      <div class="auth__pitch">
        <span class="eyebrow eyebrow--onblue"><i>%s</i>Finbolt payments, faster</span>
        <h1>%s</h1>
        <p>%s</p>
        <ul class="auth__points">
        %s
        </ul>
        <p class="auth__trust">%s Trusted by more than 10,000 businesses</p>
      </div>
""" % (I["bolt"], title, lead, items, I["shield"])


def pw_field(fid, label, autocomplete, hint=""):
    return """          <div class="field-row">
            <label for="%s">%s</label>
            <div class="field-pw">
              <input id="%s" name="%s" type="password" autocomplete="%s"
                placeholder="At least 8 characters" required>
              <button class="field-pw__toggle" type="button" data-pw-toggle
                aria-label="Show password" aria-pressed="false">%s%s</button>
            </div>
            %s
            <p class="field-err" id="%s-err" role="alert"></p>
          </div>
""" % (fid, label, fid, fid, autocomplete, I["eye"], I["eyeoff"], hint, fid)


LOGIN_FORM = """        <form class="authform" data-auth="login" novalidate>
          <div class="field-row">
            <label for="l-email">Work email</label>
            <input id="l-email" name="l-email" type="email" autocomplete="email"
              placeholder="john@company.com" required>
            <p class="field-err" id="l-email-err" role="alert"></p>
          </div>
%(pw)s
          <div class="authform__aside">
            <label class="checkline"><input type="checkbox" name="remember" checked>
              <span>Keep me signed in</span></label>
            <a class="authform__link" href="contact.html">Forgot password?</a>
          </div>
          <button class="btn btn--primary authform__submit" type="submit">Sign in%(arrow)s</button>
        </form>
""" % {"pw": pw_field("l-password", "Password", "current-password"),
       "arrow": I["arrow"]}


REGISTER_FORM = """        <form class="authform" data-auth="register" novalidate>
          <div class="form__row">
            <div class="field-row">
              <label for="r-first">First name</label>
              <input id="r-first" name="r-first" type="text" autocomplete="given-name"
                placeholder="John" required>
              <p class="field-err" id="r-first-err" role="alert"></p>
            </div>
            <div class="field-row">
              <label for="r-last">Last name</label>
              <input id="r-last" name="r-last" type="text" autocomplete="family-name"
                placeholder="Clayton" required>
              <p class="field-err" id="r-last-err" role="alert"></p>
            </div>
          </div>
          <div class="field-row">
            <label for="r-email">Work email</label>
            <input id="r-email" name="r-email" type="email" autocomplete="email"
              placeholder="john@company.com" required>
            <p class="field-err" id="r-email-err" role="alert"></p>
          </div>
          <div class="field-row">
            <label for="r-company">Business name</label>
            <input id="r-company" name="r-company" type="text" autocomplete="organization"
              placeholder="Northwind Studios" required>
            <p class="field-err" id="r-company-err" role="alert"></p>
          </div>
%(pw)s
          <label class="checkline checkline--terms">
            <input type="checkbox" name="terms" required>
            <span>I agree to the <a href="contact.html">terms of service</a> and
              <a href="contact.html">privacy policy</a>.</span>
          </label>
          <p class="field-err" id="r-terms-err" role="alert"></p>
          <button class="btn btn--primary authform__submit" type="submit">Create account%(arrow)s</button>
        </form>
""" % {"pw": pw_field("r-password", "Password", "new-password",
                      hint='<div class="strength" data-strength hidden>'
                           '<span class="strength__bars"><i></i><i></i><i></i></span>'
                           '<span class="strength__label"></span></div>'),
       "arrow": I["arrow"]}


def auth_page(mode):
    is_login = mode == "login"
    return """  <section class="band auth">
    <div class="wrap auth__grid">
%(pitch)s
      <div class="auth__card">
        <h2 class="auth__title">%(title)s</h2>
        <p class="auth__sub">%(sub)s</p>

        <div class="auth__done" data-auth-done hidden>
          <span class="auth__done-mark">%(check)s</span>
          <h3>%(donetitle)s</h3>
          <p>%(donebody)s</p>
          <a class="btn btn--ghost" href="index.html">Back to the site%(arrow)s</a>
        </div>

%(form)s
        <p class="auth__swap">%(swap)s</p>
        <p class="auth__note">This is a front-end demo &mdash; no account is created and
          nothing is sent anywhere. Point the form at your own backend before going live.</p>
      </div>
    </div>
  </section>
""" % {
        "pitch": auth_pitch(mode),
        "title": "Sign in" if is_login else "Create your account",
        "sub": ("Welcome back. Enter your details to reach your dashboard."
                if is_login else
                "Four minutes to your first payment. No card needed."),
        "check": I["check"], "arrow": I["arrow"],
        "donetitle": "Signed in" if is_login else "Account created",
        "donebody": ("In the real product this is where your dashboard would load."
                     if is_login else
                     "In the real product we would email you a link to confirm this "
                     "address and set your account live."),
        "form": LOGIN_FORM if is_login else REGISTER_FORM,
        "swap": ('New to Finbolt? <a href="register.html">Create an account</a>'
                 if is_login else
                 'Already have an account? <a href="login.html">Sign in</a>'),
    }


LOGIN_PAGE = auth_page("login")
REGISTER_PAGE = auth_page("register")


# --------------------------------------------------------------------------
# Write
# --------------------------------------------------------------------------
PAGES = [
    ("index.html", "Finbolt — Make your business payment fast and secure",
     "Finbolt is one account for invoices, cards, transfers and payouts. Live in four minutes, settled the same day.",
     HOME),
    ("about.html", "About Finbolt — a payments company that started as a spreadsheet",
     "Where Finbolt came from, what we believe, and how we grew to serve more than 10,000 businesses.",
     ABOUT),
    ("benefits.html", "Benefits and pricing — Finbolt",
     "Same-day settlement, every payment method, eleven currencies and fraud screening on by default.",
     BENEFITS_PAGE),
    ("testimonials.html", "Testimonials — what businesses say about Finbolt",
     "Reviews from finance leads, founders and freelancers using Finbolt to get paid.",
     TESTIMONIALS_PAGE),
    ("career.html", "Careers at Finbolt",
     "Six open roles across engineering, design, compliance, support and growth.",
     CAREER_PAGE),
    ("blog.html", "Blog — notes on money, fraud and getting paid",
     "What we learn running payments for ten thousand businesses.",
     BLOG_PAGE),
    ("support.html", "Support centre — Finbolt",
     "Answers to common questions, plus live chat, email and phone support.",
     SUPPORT_PAGE),
    ("contact.html", "Contact Finbolt",
     "Talk to sales or support about opening an account, pricing or a payment.",
     CONTACT_PAGE),
    ("login.html", "Log in to Finbolt",
     "Sign in to your Finbolt account to see settlements, invoices and payouts.",
     LOGIN_PAGE),
    ("register.html", "Create your Finbolt account",
     "Open a Finbolt account in about four minutes. Free for 30 days, no card needed.",
     REGISTER_PAGE),
]

def render(fname, title, desc, main):
    return SHELL.format(title=title, desc=desc,
                        header=header(fname), main=main, footer=FOOTER)


def write_all():
    for fname, title, desc, main in PAGES:
        html = render(fname, title, desc, main)
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", fname, len(html), "bytes")


# Importable: package.py reads PAGES to build the WordPress templates from the
# same section markup, so the two products can never drift apart.
if __name__ == "__main__":
    write_all()
