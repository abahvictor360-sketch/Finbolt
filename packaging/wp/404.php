<?php
/**
 * Not found.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php esc_html_e( '404', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php esc_html_e( 'We cannot find that page', 'finbolt' ); ?></h1>
      <p><?php esc_html_e( 'The link may be old, or the page may have moved. Try a search, or start again from the homepage.', 'finbolt' ); ?></p>
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php esc_html_e( 'Not found', 'finbolt' ); ?></span></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap" style="max-width:560px">
      <div class="fcard reveal" style="text-align:center">
        <h3><?php esc_html_e( 'Search instead', 'finbolt' ); ?></h3>
        <?php get_search_form(); ?>
      </div>
      <p style="text-align:center;margin-top:26px">
        <a class="btn btn--primary" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Back to the homepage', 'finbolt' ); ?><?php echo finbolt_icon( 'arrow' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup. ?></a>
      </p>
    </div>
  </section>
<?php
get_footer();
