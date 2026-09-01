=== Finbolt ===
Contributors: finbolt
Requires at least: 6.0
Tested up to: 6.7
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html
Tags: two-columns, right-sidebar, custom-menu, custom-colors, featured-images, translation-ready, blog, business

A payments and fintech marketing theme with ten page templates on one design system.

== Description ==

Finbolt is a marketing theme for payments, fintech and SaaS businesses. Eight
page templates plus a real blog share one design system: a blue gradient band, a
floating card frame, staggered scroll reveals and counting figures.

The theme ships with three menu locations, a blog sidebar, and a customizer
panel for the wordmark, three palette colours, the call-to-action button and
link, and the footer blurb, contact details and social profiles.

Animation is disabled for visitors who ask for reduced motion. Every text
element in the design meets WCAG AA contrast, and the layout is verified from
320px to 1920px.

== Installation ==

1. Appearance > Themes > Add New > Upload Theme, choose finbolt.zip, Install,
   then Activate.
2. Appearance > Menus: create a menu and assign it to "Primary (header and
   drawer)". Until you do, the header falls back to the theme's own page list.
3. Create a page for each template you want and assign it under Page Attributes
   > Template — for example a page called About using "Finbolt — About".
4. Settings > Reading: set a static homepage, and set the Posts page to an empty
   page called Blog. The homepage uses front-page.php automatically.
5. Appearance > Customize > Finbolt theme: set the wordmark, colours, button
   link and footer details.

== Frequently Asked Questions ==

= The header navigation shows pages I have not created =

Before a menu is assigned, the header lists the pages the design ships with and
links them by slug. Assign a menu to "Primary" and it takes over completely.

= Do the login and register templates create accounts? =

No. They are the design's front-end forms: they validate input and show a
confirmation, but no account is created and nothing is sent. WordPress has its
own authentication — to use it, set the customizer's button and log-in links to
your registration and wp-login.php URLs.

= Where do the homepage sections come from? =

front-page.php holds them as markup. Edit that file, or rebuild the section
copy from the HTML template's build.py and repackage.

= Can I change the colours? =

Appearance > Customize > Finbolt theme > Colours sets three design tokens, which
every page reads. For anything finer, edit the custom properties at the top of
assets/css/style.css.

== Changelog ==

= 1.0.0 =
* Initial release.

== Copyright ==

Finbolt WordPress theme, 1.0.0, is distributed under the terms of the GNU GPL
version 2 or later.

Plus Jakarta Sans and Inter are licensed under the SIL Open Font License 1.1 and
load from Google Fonts. All icons are original inline SVG written for this theme.
The theme ships no raster images. All demo copy, statistics and company names are
invented placeholders.
