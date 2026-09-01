#!/usr/bin/env python3
"""Build the two sellable products from this one source tree.

  dist/finbolt-html-<version>.zip        static HTML template + documentation
  dist/finbolt-wordpress-<version>.zip   installable WordPress theme

The WordPress page templates are generated from build.PAGES, the same section
markup the static pages use, so the two products cannot drift apart.
"""

import os
import re
import shutil
import subprocess
import sys

import build

VERSION = "1.0.0"
ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
WPSRC = os.path.join(ROOT, "packaging", "wp")
DOCSRC = os.path.join(ROOT, "packaging", "docs")

# Pages that become WordPress page templates. Home gets front-page.php; the
# blog is served by index.php from real posts, so it has no template here.
WP_TEMPLATES = {
    "about.html": "About",
    "benefits.html": "Benefits",
    "testimonials.html": "Testimonials",
    "career.html": "Career",
    "support.html": "Support",
    "contact.html": "Contact",
    "login.html": "Log in",
    "register.html": "Register",
}

LINK = re.compile(r'href="([a-z0-9\-]+)\.html"')


def phpify(markup):
    """Rewrite static page links to resolve through the theme at runtime."""
    return LINK.sub(
        lambda m: 'href="<?php echo esc_url( finbolt_link( \'%s\' ) ); ?>"' % m.group(1),
        markup,
    )


def clean(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copy_assets(dest):
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(dest, "assets"))
    # A real file, not a dotfile: zip skips dotfiles, and the buyer should find
    # this folder waiting for their artwork.
    img = os.path.join(dest, "assets", "img")
    os.makedirs(img, exist_ok=True)
    with open(os.path.join(img, "README.txt"), "w", encoding="utf-8") as f:
        f.write("Drop your own images here.\n\n"
                "The template ships with none - every illustration is a CSS gradient\n"
                "or inline SVG, so there is nothing to optimise or replace.\n")


# ---------------------------------------------------------------------------
# HTML template package
# ---------------------------------------------------------------------------
def build_html(stage):
    root = os.path.join(stage, "finbolt-html-template")
    tpl = os.path.join(root, "template")
    os.makedirs(tpl)

    build.write_all()
    for fname, _t, _d, _m in build.PAGES:
        shutil.copy2(os.path.join(ROOT, fname), os.path.join(tpl, fname))
    copy_assets(tpl)
    shutil.copy2(os.path.join(ROOT, "build.py"), os.path.join(tpl, "build.py"))

    os.makedirs(os.path.join(root, "documentation"))
    shutil.copy2(os.path.join(DOCSRC, "documentation.html"),
                 os.path.join(root, "documentation", "index.html"))

    os.makedirs(os.path.join(root, "licensing"))
    for name in ("LICENSE.txt", "EULA.txt", "GPL-2.0.txt", "third-party-assets.txt"):
        shutil.copy2(os.path.join(DOCSRC, name), os.path.join(root, "licensing", name))

    shutil.copy2(os.path.join(DOCSRC, "CHANGELOG.txt"), os.path.join(root, "CHANGELOG.txt"))
    shutil.copy2(os.path.join(DOCSRC, "readme-html.txt"), os.path.join(root, "README.txt"))
    return root


# ---------------------------------------------------------------------------
# WordPress theme package
# ---------------------------------------------------------------------------
def build_wp(stage):
    theme = os.path.join(stage, "finbolt")
    shutil.copytree(WPSRC, theme)
    copy_assets(theme)

    pages = dict((f, (t, d, m)) for f, t, d, m in build.PAGES)

    # Home
    _t, _d, home = pages["index.html"]
    write_template(
        os.path.join(theme, "front-page.php"),
        header='/**\n * The homepage.\n *\n * @package Finbolt\n */',
        markup=home,
    )

    tdir = os.path.join(theme, "page-templates")
    os.makedirs(tdir, exist_ok=True)
    for fname, label in WP_TEMPLATES.items():
        slug = fname[:-5]
        _t, _d, markup = pages[fname]
        write_template(
            os.path.join(tdir, slug + ".php"),
            header=('/**\n * Template Name: Finbolt — %s\n *\n * @package Finbolt\n */'
                    % label),
            markup=markup,
        )

    shutil.copy2(os.path.join(DOCSRC, "readme-wp.txt"), os.path.join(theme, "readme.txt"))
    # A GPL-licensed theme has to distribute the licence text with it.
    shutil.copy2(os.path.join(DOCSRC, "GPL-2.0.txt"), os.path.join(theme, "LICENSE"))
    shutil.copy2(os.path.join(DOCSRC, "CHANGELOG.txt"), os.path.join(theme, "CHANGELOG.txt"))
    if os.path.exists(os.path.join(DOCSRC, "screenshot.png")):
        shutil.copy2(os.path.join(DOCSRC, "screenshot.png"),
                     os.path.join(theme, "screenshot.png"))
    return theme


def write_template(path, header, markup):
    body = "<?php\n%s\n\ndefined( 'ABSPATH' ) || exit;\n\nget_header();\n?>\n%s<?php\nget_footer();\n" % (
        header, phpify(markup))
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def check_theme(theme):
    """Lint every PHP file, then render every template against WordPress stubs.

    A theme that does not execute is not shippable, so this gates the zip.
    """
    php = shutil.which("php")
    if not php:
        print("!! php not found - skipping the theme render check")
        return

    for base, _dirs, files in os.walk(theme):
        for name in sorted(files):
            if name.endswith(".php"):
                subprocess.check_call([php, "-l", os.path.join(base, name)],
                                      stdout=subprocess.DEVNULL)

    harness = os.path.join(ROOT, "packaging", "tests", "render.php")
    # Three states: Elementor absent, Elementor active, and Elementor Theme
    # Builder supplying the header, footer, single and archive. The last one
    # proves the theme stands down instead of rendering a second header.
    for mode in ([], ["--elementor"], ["--takeover"]):
        subprocess.check_call([php, harness, theme] + mode,
                              stdout=subprocess.DEVNULL)
    subprocess.check_call([php, harness, theme])


def zip_up(stage, inner, name):
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, name)
    if os.path.exists(out):
        os.remove(out)
    subprocess.check_call(
        ["zip", "-qr", "-X", out, inner, "-x", ".*", "-x", "*/.*"],
        cwd=stage,
    )
    return out


def main():
    clean(DIST)
    stage = os.path.join(DIST, "_stage")

    html_stage = os.path.join(stage, "html")
    os.makedirs(html_stage)
    html_root = build_html(html_stage)
    html_zip = zip_up(html_stage, os.path.basename(html_root),
                      "finbolt-html-%s.zip" % VERSION)

    wp_stage = os.path.join(stage, "wp")
    os.makedirs(wp_stage)
    theme = build_wp(wp_stage)
    check_theme(theme)
    wp_zip = zip_up(wp_stage, os.path.basename(theme),
                    "finbolt-wordpress-%s.zip" % VERSION)

    shutil.rmtree(stage)
    for path in (html_zip, wp_zip):
        print("%-42s %8.1f KB" % (os.path.basename(path), os.path.getsize(path) / 1024.0))


if __name__ == "__main__":
    sys.exit(main())
