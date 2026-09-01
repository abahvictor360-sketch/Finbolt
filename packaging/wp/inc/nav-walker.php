<?php
/**
 * Flat navigation walker.
 *
 * The design uses a bare row of anchors inside a pill, not a nested list, so
 * this walker drops the list markup and marks the current item for the CSS.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

/**
 * Outputs menu items as plain anchors.
 */
class Finbolt_Nav_Walker extends Walker_Nav_Menu {

	/**
	 * No sub-lists: the header nav is deliberately one level deep.
	 *
	 * @param string $output Passed by reference.
	 * @param int    $depth  Depth of the item.
	 * @param array  $args   Menu arguments.
	 */
	public function start_lvl( &$output, $depth = 0, $args = null ) {}

	/**
	 * No sub-lists.
	 *
	 * @param string $output Passed by reference.
	 * @param int    $depth  Depth of the item.
	 * @param array  $args   Menu arguments.
	 */
	public function end_lvl( &$output, $depth = 0, $args = null ) {}

	/**
	 * Render one item as an anchor.
	 *
	 * @param string  $output Passed by reference.
	 * @param WP_Post $item   Menu item.
	 * @param int     $depth  Depth of the item.
	 * @param array   $args   Menu arguments.
	 * @param int     $id     Current item ID.
	 */
	public function start_el( &$output, $item, $depth = 0, $args = null, $id = 0 ) {
		if ( $depth > 0 ) {
			return;
		}

		$classes = (array) $item->classes;
		$current = in_array( 'current-menu-item', $classes, true )
			|| in_array( 'current_page_item', $classes, true )
			|| in_array( 'current-menu-ancestor', $classes, true );

		$output .= sprintf(
			'<a href="%1$s"%2$s%3$s>%4$s</a>',
			esc_url( $item->url ),
			$current ? ' aria-current="page"' : '',
			$item->target ? ' target="' . esc_attr( $item->target ) . '"' : '',
			esc_html( $item->title )
		);
	}

	/**
	 * Anchors need no closing wrapper.
	 *
	 * @param string  $output Passed by reference.
	 * @param WP_Post $item   Menu item.
	 * @param int     $depth  Depth of the item.
	 * @param array   $args   Menu arguments.
	 */
	public function end_el( &$output, $item, $depth = 0, $args = null ) {}
}
