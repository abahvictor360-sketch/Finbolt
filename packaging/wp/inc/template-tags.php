<?php
/**
 * Template helpers.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

/**
 * Resolve one of the theme's marketing pages to a real permalink.
 *
 * The static template links pages as "about.html". In WordPress the same link
 * has to find whichever page the site owner assigned that page template to, so
 * this looks for the template first, then a matching slug, and only then falls
 * back to a guessed path.
 *
 * @param string $slug Page key, e.g. "about" or "index".
 * @return string
 */
function finbolt_link( $slug ) {
	static $cache = array();

	$slug = sanitize_key( $slug );

	if ( 'index' === $slug ) {
		return home_url( '/' );
	}

	if ( isset( $cache[ $slug ] ) ) {
		return $cache[ $slug ];
	}

	$url = '';

	if ( 'blog' === $slug ) {
		$posts_page = (int) get_option( 'page_for_posts' );
		if ( $posts_page ) {
			$url = get_permalink( $posts_page );
		}
	}

	if ( ! $url ) {
		$pages = get_pages(
			array(
				'meta_key'    => '_wp_page_template',
				'meta_value'  => 'page-templates/' . $slug . '.php',
				'number'      => 1,
				'post_status' => 'publish',
			)
		);
		if ( ! empty( $pages ) ) {
			$url = get_permalink( $pages[0] );
		}
	}

	if ( ! $url ) {
		$page = get_page_by_path( $slug );
		if ( $page ) {
			$url = get_permalink( $page );
		}
	}

	if ( ! $url ) {
		$url = home_url( '/' . $slug . '/' );
	}

	$cache[ $slug ] = $url;
	return $url;
}

/**
 * The brand lockup, using a custom logo when one is set.
 *
 * @param string $class Extra classes for the anchor.
 */
function finbolt_brand( $class = '' ) {
	$mark = '<span class="brand__mark"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></span>';

	if ( has_custom_logo() ) {
		$logo_id = (int) get_theme_mod( 'custom_logo' );
		$img     = wp_get_attachment_image(
			$logo_id,
			'full',
			false,
			array(
				'class' => 'brand__logo',
				'alt'   => esc_attr( get_bloginfo( 'name' ) ),
			)
		);
		if ( $img ) {
			$mark = $img;
		}
	}

	printf(
		'<a class="brand %1$s" href="%2$s">%3$s%4$s</a>',
		esc_attr( $class ),
		esc_url( home_url( '/' ) ),
		$mark, // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- built above from escaped parts.
		esc_html( get_theme_mod( 'finbolt_brand_name', get_bloginfo( 'name' ) ) )
	);
}

/**
 * The header/drawer navigation, falling back to the theme's own page list so a
 * freshly activated theme is never left with an empty header.
 *
 * @param string $location Menu location key.
 * @param string $aria     Accessible label.
 */
function finbolt_nav( $location = 'primary', $aria = 'Primary' ) {
	if ( has_nav_menu( $location ) ) {
		wp_nav_menu(
			array(
				'theme_location' => $location,
				'container'      => false,
				'items_wrap'     => '%3$s',
				'depth'          => 1,
				'walker'         => new Finbolt_Nav_Walker(),
				'fallback_cb'    => false,
			)
		);
		return;
	}

	foreach ( finbolt_default_pages() as $slug => $label ) {
		$url     = finbolt_link( $slug );
		$current = untrailingslashit( $url ) === untrailingslashit( finbolt_current_url() );
		printf(
			'<a href="%1$s"%2$s>%3$s</a>',
			esc_url( $url ),
			$current ? ' aria-current="page"' : '',
			esc_html( $label )
		);
	}
}

/**
 * The pages the static template ships with, used for the menu fallback.
 *
 * @return array
 */
function finbolt_default_pages() {
	return array(
		'index'        => __( 'Home', 'finbolt' ),
		'about'        => __( 'About', 'finbolt' ),
		'benefits'     => __( 'Benefits', 'finbolt' ),
		'testimonials' => __( 'Testimonials', 'finbolt' ),
		'career'       => __( 'Career', 'finbolt' ),
		'blog'         => __( 'Blog', 'finbolt' ),
		'support'      => __( 'Support', 'finbolt' ),
		'contact'      => __( 'Contact', 'finbolt' ),
	);
}

/**
 * Current request URL, used only to mark the active nav item in the fallback.
 *
 * @return string
 */
function finbolt_current_url() {
	if ( is_front_page() ) {
		return home_url( '/' );
	}
	$id = get_queried_object_id();
	return $id ? (string) get_permalink( $id ) : home_url( '/' );
}

/**
 * A footer link column: an assigned menu, or the shipped defaults.
 *
 * @param string $location Menu location key.
 * @param array  $fallback slug => label pairs.
 */
function finbolt_footer_links( $location, $fallback ) {
	if ( has_nav_menu( $location ) ) {
		wp_nav_menu(
			array(
				'theme_location' => $location,
				'container'      => false,
				'items_wrap'     => '%3$s',
				'depth'          => 1,
				'walker'         => new Finbolt_Nav_Walker(),
				'fallback_cb'    => false,
			)
		);
		return;
	}

	foreach ( $fallback as $slug => $label ) {
		printf( '<a href="%1$s">%2$s</a>', esc_url( finbolt_link( $slug ) ), esc_html( $label ) );
	}
}

/**
 * Where the "Get started" button points.
 *
 * @return string
 */
function finbolt_cta_url() {
	$url = trim( (string) get_theme_mod( 'finbolt_cta_url', '' ) );
	return $url ? $url : finbolt_link( 'register' );
}

/**
 * Where the "Log in" link points.
 *
 * @return string
 */
function finbolt_login_url() {
	$url = trim( (string) get_theme_mod( 'finbolt_login_url', '' ) );
	return $url ? $url : finbolt_link( 'login' );
}

/**
 * One reusable inline SVG, so markup does not repeat the path data.
 *
 * @param string $name Icon key.
 * @return string
 */
function finbolt_icon( $name ) {
	$open  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
	$icons = array(
		'arrow' => '<path d="M5 12h13"/><path d="m12 5 7 7-7 7"/>',
		'clock' => '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3 2"/>',
		'tag'   => '<path d="M20.5 13.5 13 21l-9-9V4h8l8.5 8.5Z"/><path d="M8 8v.01"/>',
		'chart' => '<path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/>',
	);
	if ( ! isset( $icons[ $name ] ) ) {
		return '';
	}
	return $open . $icons[ $name ] . '</svg>';
}
