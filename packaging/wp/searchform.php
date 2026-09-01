<?php
/**
 * Search form in the design's field style.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

$finbolt_id = 'finbolt-search-' . wp_unique_id();
?>
<form role="search" method="get" class="form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
  <label class="screen-reader-text" for="<?php echo esc_attr( $finbolt_id ); ?>"><?php esc_html_e( 'Search', 'finbolt' ); ?></label>
  <input id="<?php echo esc_attr( $finbolt_id ); ?>" type="search" name="s"
    value="<?php echo esc_attr( get_search_query() ); ?>"
    placeholder="<?php esc_attr_e( 'Search the blog', 'finbolt' ); ?>">
  <button class="btn btn--primary" type="submit" style="justify-content:center"><?php esc_html_e( 'Search', 'finbolt' ); ?></button>
</form>
