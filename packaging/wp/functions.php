<?php
/**
 * Finbolt theme setup.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

define( 'FINBOLT_VERSION', '1.0.0' );

require_once get_template_directory() . '/inc/nav-walker.php';
require_once get_template_directory() . '/inc/template-tags.php';
require_once get_template_directory() . '/inc/customizer.php';
require_once get_template_directory() . '/inc/elementor.php';

/**
 * Theme supports, menus and content width.
 */
function finbolt_setup() {
	load_theme_textdomain( 'finbolt', get_template_directory() . '/languages' );

	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'customize-selective-refresh-widgets' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'align-wide' );
	add_theme_support(
		'html5',
		array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' )
	);
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 34,
			'width'       => 34,
			'flex-height' => true,
			'flex-width'  => true,
		)
	);

	register_nav_menus(
		array(
			'primary'        => __( 'Primary (header and drawer)', 'finbolt' ),
			'footer-product' => __( 'Footer column: Product', 'finbolt' ),
			'footer-company' => __( 'Footer column: Company', 'finbolt' ),
		)
	);

	// The design is a fixed-width card, so wide content has a hard ceiling.
	$GLOBALS['content_width'] = 1120;
}
add_action( 'after_setup_theme', 'finbolt_setup' );

/**
 * Front-end styles and scripts.
 */
function finbolt_assets() {
	wp_enqueue_style(
		'finbolt-fonts',
		'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'finbolt-design',
		get_template_directory_uri() . '/assets/css/style.css',
		array(),
		FINBOLT_VERSION
	);

	wp_enqueue_style(
		'finbolt-style',
		get_stylesheet_uri(),
		array( 'finbolt-design' ),
		FINBOLT_VERSION
	);

	$overrides = finbolt_color_overrides();
	if ( $overrides ) {
		wp_add_inline_style( 'finbolt-style', $overrides );
	}

	wp_enqueue_script(
		'finbolt-script',
		get_template_directory_uri() . '/assets/js/main.js',
		array(),
		FINBOLT_VERSION,
		true
	);

	// The capture fields hand the address to whichever page holds the register
	// template, so the script must not assume a static register.html.
	wp_localize_script(
		'finbolt-script',
		'FINBOLT',
		array( 'registerUrl' => finbolt_cta_url() )
	);

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
}
add_action( 'wp_enqueue_scripts', 'finbolt_assets' );

/**
 * Editor styles so the block editor matches the front end.
 */
function finbolt_editor_assets() {
	add_theme_support( 'editor-styles' );
	add_editor_style( 'assets/css/style.css' );
}
add_action( 'after_setup_theme', 'finbolt_editor_assets' );

/**
 * Read the marketing pages' body classes onto the WordPress body tag.
 *
 * @param array $classes Existing classes.
 * @return array
 */
function finbolt_body_classes( $classes ) {
	if ( ! is_active_sidebar( 'sidebar-1' ) ) {
		$classes[] = 'no-sidebar';
	}
	return $classes;
}
add_filter( 'body_class', 'finbolt_body_classes' );

/**
 * Blog sidebar.
 */
function finbolt_widgets() {
	register_sidebar(
		array(
			'name'          => __( 'Blog sidebar', 'finbolt' ),
			'id'            => 'sidebar-1',
			'description'   => __( 'Shown beside single posts and the blog archive.', 'finbolt' ),
			'before_widget' => '<section id="%1$s" class="widget fcard %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h4 class="widget__title">',
			'after_title'   => '</h4>',
		)
	);
}
add_action( 'widgets_init', 'finbolt_widgets' );

/**
 * Pagination in the design's pill style.
 */
function finbolt_pagination() {
	the_posts_pagination(
		array(
			'mid_size'  => 1,
			'class'     => 'pagination',
			'prev_text' => esc_html__( 'Previous', 'finbolt' ),
			'next_text' => esc_html__( 'Next', 'finbolt' ),
		)
	);
}

/**
 * Excerpt length tuned to the card layout.
 *
 * @param int $length Incoming length.
 * @return int
 */
function finbolt_excerpt_length( $length ) {
	return is_admin() ? $length : 24;
}
add_filter( 'excerpt_length', 'finbolt_excerpt_length' );

/**
 * Excerpt ellipsis.
 *
 * @param string $more Incoming string.
 * @return string
 */
function finbolt_excerpt_more( $more ) {
	return is_admin() ? $more : '&hellip;';
}
add_filter( 'excerpt_more', 'finbolt_excerpt_more' );
