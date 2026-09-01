<?php
/**
 * Template Name: Finbolt — Elementor (full width)
 *
 * A page with no heading band, no section padding and no card frame, so
 * Elementor controls the whole canvas between the header and the footer.
 * Sections can run edge to edge, and sticky elements work because nothing
 * above them sets overflow.
 *
 * The theme's header and footer still render, so navigation stays consistent.
 * For a page with neither, use Elementor's own "Elementor Canvas" template.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();

while ( have_posts() ) :
	the_post();
	the_content();
endwhile;

get_footer();
