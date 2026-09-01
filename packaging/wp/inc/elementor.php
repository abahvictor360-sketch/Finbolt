<?php
/**
 * Elementor compatibility.
 *
 * Three things make a theme genuinely usable with Elementor:
 *
 *   1. Theme Builder locations, so Elementor Pro can take over the header,
 *      footer, single and archive templates instead of fighting the theme's.
 *   2. A page template with no content wrapper, so sections can run full width.
 *   3. Getting out of the way inside the editor, where the theme's scroll
 *      reveals would otherwise leave freshly dropped widgets invisible.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

/**
 * Is Elementor active?
 *
 * @return bool
 */
function finbolt_has_elementor() {
	return did_action( 'elementor/loaded' ) > 0;
}

/**
 * Are we rendering inside the Elementor editor or its preview frame?
 *
 * @return bool
 */
function finbolt_in_elementor_editor() {
	if ( ! finbolt_has_elementor() || ! class_exists( '\Elementor\Plugin' ) ) {
		return false;
	}
	$plugin = \Elementor\Plugin::$instance;

	if ( isset( $plugin->editor ) && $plugin->editor->is_edit_mode() ) {
		return true;
	}
	if ( isset( $plugin->preview ) && $plugin->preview->is_preview_mode() ) {
		return true;
	}
	return false;
}

/**
 * Register the Theme Builder locations Elementor Pro can override.
 *
 * @param \ElementorPro\Modules\ThemeBuilder\Classes\Locations_Manager $manager Location manager.
 */
function finbolt_register_elementor_locations( $manager ) {
	$manager->register_all_core_location();
}
add_action( 'elementor/theme/register_locations', 'finbolt_register_elementor_locations' );

/**
 * Ask Elementor to render a Theme Builder location.
 *
 * @param string $location Location name: header, footer, single, archive.
 * @return bool True when Elementor rendered it and the theme should stand down.
 */
function finbolt_elementor_location( $location ) {
	if ( ! function_exists( 'elementor_theme_do_location' ) ) {
		return false;
	}
	return elementor_theme_do_location( $location );
}

/**
 * Body classes that tell the stylesheet how much of the design to stand down.
 *
 * @param array $classes Existing classes.
 * @return array
 */
function finbolt_elementor_body_classes( $classes ) {
	if ( finbolt_has_elementor() ) {
		$classes[] = 'finbolt-elementor';
	}
	if ( finbolt_in_elementor_editor() ) {
		$classes[] = 'finbolt-editing';
	}
	if ( is_page_template( 'page-templates/builder.php' ) ) {
		// The card frame clips full-bleed sections and breaks sticky elements,
		// so builder pages drop it.
		$classes[] = 'finbolt-frameless';
	}
	return $classes;
}
add_filter( 'body_class', 'finbolt_elementor_body_classes' );

/**
 * Elementor reads this for its default content width.
 */
function finbolt_elementor_content_width() {
	if ( ! finbolt_has_elementor() ) {
		return;
	}
	// Matches --wrap in assets/css/style.css.
	if ( ! isset( $GLOBALS['content_width'] ) ) {
		$GLOBALS['content_width'] = 1120;
	}
}
add_action( 'template_redirect', 'finbolt_elementor_content_width' );

/**
 * Tell the front-end script to leave the page alone while it is being edited.
 *
 * The reveal animation starts elements at opacity 0. In the editor that would
 * make a widget invisible until something scrolled, which reads as a bug.
 */
function finbolt_elementor_editor_flag() {
	if ( ! finbolt_in_elementor_editor() ) {
		return;
	}
	wp_add_inline_script(
		'finbolt-script',
		'window.FINBOLT = window.FINBOLT || {}; window.FINBOLT.editing = true;',
		'before'
	);
}
add_action( 'wp_enqueue_scripts', 'finbolt_elementor_editor_flag', 20 );
