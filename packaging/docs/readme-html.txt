Finbolt — HTML template
=======================
Version 1.0.0

WHAT IS IN THIS PACKAGE
-----------------------
  template/         The site. Ten pages, one stylesheet, one script.
  documentation/    Open index.html in a browser.
  licensing/        EULA.txt (the HTML template's commercial licence),
                    GPL-2.0.txt (the WordPress theme's licence), an overview
                    and third-party asset credits.
  CHANGELOG.txt

QUICK START
-----------
Open template/index.html in a browser. That is all — there is no build step,
no dependencies and no server required.

To serve it locally over http (needed if you add anything that fetches files):

    cd template
    python3 -m http.server 8000

Then open http://localhost:8000

EDITING
-------
Two routes, and you should pick one:

  1. Edit the HTML directly. The files are plain and readable. If you take this
     route, delete template/build.py so nobody regenerates over your work.

  2. Edit build.py and regenerate. Copy, icons and page structure live in Python
     lists near the top of the file. Run `python3 build.py` and all ten pages
     rewrite with the shared header and footer intact. Safer while the site is
     still growing.

Colours, type and spacing are all custom properties at the top of
assets/css/style.css. Change them there and every page follows.

BEFORE YOU GO LIVE
------------------
  * The contact form, the email capture fields and the login/register forms are
    front-end only. They validate properly but create no account and send
    nothing. Connect them to your own backend or a form service.
  * All statistics, quotes, job listings and partner names are placeholders.
  * Replace the inline SVG favicon in each page's <head> with a real icon file.

Full detail is in documentation/index.html.
