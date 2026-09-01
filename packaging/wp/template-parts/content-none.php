<?php
/**
 * Shown when a loop returns nothing.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;
?>
<div class="fcard reveal" style="max-width:560px;margin-inline:auto;text-align:center">
  <h3><?php esc_html_e( 'Nothing here yet', 'finbolt' ); ?></h3>
  <p><?php esc_html_e( 'No posts matched. Try another search, or head back to the homepage.', 'finbolt' ); ?></p>
  <?php get_search_form(); ?>
</div>
