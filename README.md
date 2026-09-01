# Finbolt

Marketing site for **Finbolt**, a payments product. Eight static pages, one shared
stylesheet, no build step and no dependencies — open `index.html` and it runs.

## Pages

| Page | File | What's on it |
| --- | --- | --- |
| Home | `index.html` | Hero, trusted-by marquee, audience tabs, invoice showcase, security section, speed split, CTA |
| About | `about.html` | Story, stats, values grid, company timeline |
| Benefits | `benefits.html` | Six benefits, settlement breakdown, three pricing plans |
| Testimonials | `testimonials.html` | Featured quote, review stats, six customer quotes |
| Career | `career.html` | Why Finbolt, team stats, six open roles, perks |
| Blog | `blog.html` | Featured long read, six-post grid |
| Support | `support.html` | Six help categories, FAQ accordion, three contact channels |
| Contact | `contact.html` | Contact form, office details, quick answers |
| Log in | `login.html` | Sign-in form beside a value panel on the blue band |
| Register | `register.html` | Sign-up form, password strength meter, terms gate |

Every page shares the same header, footer, blue gradient band and CTA, so the design
stays identical as pages are added.

## Structure

```
.
├── index.html            about.html      benefits.html   testimonials.html
├── career.html           blog.html       support.html    contact.html
├── login.html            register.html
├── assets/
│   ├── css/style.css     all design tokens, components and breakpoints
│   └── js/main.js        drawer, tabs, accordion, scroll reveal, forms
├── build.py              regenerates every page from one shared shell
└── README.md
```

## Design system

Tokens live at the top of `assets/css/style.css`. Change them there and every page
follows.

**Colour**

| Token | Value | Used for |
| --- | --- | --- |
| `--blue` | `#1B6DF0` | Primary actions, links, accent words in headings |
| `--blue-deep` | `#0B45C4` | Bottom of the gradient band, logo mark |
| `--blue-tint` | `#E9F1FE` | Eyebrow pills, icon tiles |
| `--blue-wash` | `#F5F8FE` | Alternating section background, form fields |
| `--ink` | `#0B1220` | Headings |
| `--ink-soft` | `#46506B` | Body copy |
| `--muted` | `#7C879F` | Secondary and caption text |
| `--line` | `#E7EBF3` | Card hairlines |

**Type** — Plus Jakarta Sans (600/700/800) for headings and figures, Inter
(400/500/600/700) for body and UI. Both load from Google Fonts. Sizes are fluid via
`clamp()`, so the scale holds from 320px to 1440px.

**Shape** — 10 / 16 / 22 / 30px radii, plus fully rounded pills for buttons and tags.

## Editing

Two options:

1. **Edit the HTML directly.** The files are plain and readable. If you do this, delete
   `build.py` so nobody regenerates over your changes.
2. **Edit `build.py` and regenerate.** Copy, icons and page structure live in Python
   lists near the top. Run `python3 build.py` and all eight pages rewrite with the
   shared header and footer intact. This is the safer route while the site is growing.

## Running locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Notes before going live

- The contact form, the email capture fields and the login/register forms are
  front-end only. They validate properly but create no account and send nothing —
  point them at your own backend, Supabase Auth, Formspree or similar before launch.
- The header "Get started" opens `register.html`, and the hero and CTA email fields
  carry the address into it as `register.html?email=...`, which the form reads and
  prefills.
- Partner names in the trusted-by strip are placeholders — swap in your real logos.
- All statistics, quotes and job listings are sample content.
- Replace the inline SVG favicon in each `<head>` with a real icon file.

## Deploying

Any static host works. For GitHub Pages: push to `main`, then Settings → Pages →
Source: *Deploy from a branch* → `main` / `root`.

## Licence

MIT.
