<?php
/**
 * Closes every page.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

$finbolt_socials = array(
	'finbolt_social_x'  => array( 'X', '<path d="M6 6l12 12M18 6 6 18"/>', false ),
	'finbolt_social_in' => array( 'LinkedIn', '<path d="M5 9v10M5 5.2v.1M10 19v-5.5a2.5 2.5 0 0 1 5 0V19M10 19v-9"/>', false ),
	'finbolt_social_fb' => array( 'Facebook', '<path d="M14.5 8.5H17V5h-2.5A4 4 0 0 0 10.5 9v2H8v3.5h2.5V22H14v-7.5h2.6l.4-3.5H14V9.5a1 1 0 0 1 .5-1Z"/>', true ),
	'finbolt_social_ig' => array( 'Instagram', '<rect x="4" y="4" width="16" height="16" rx="4.6"/><circle cx="12" cy="12" r="3.4"/><path d="M16.8 7.3v.1"/>', false ),
);

$finbolt_email = get_theme_mod( 'finbolt_email', 'hello@finbolt.com' );
$finbolt_phone = get_theme_mod( 'finbolt_phone', '+234 700 346 6538' );
?>
  </main>

  <footer class="footer">
    <div class="wrap footer__grid">
      <div>
        <p class="footer__blurb"><?php echo wp_kses_post( get_theme_mod( 'finbolt_footer_blurb', __( 'Finbolt is built on one idea: getting paid should be the simplest part of running a business.', 'finbolt' ) ) ); ?></p>
        <?php finbolt_brand(); ?>
      </div>
      <div>
        <h4><?php esc_html_e( 'Product', 'finbolt' ); ?></h4>
        <div class="footer__links">
          <?php
          finbolt_footer_links(
            'footer-product',
            array(
              'index'        => __( 'Home', 'finbolt' ),
              'benefits'     => __( 'Benefits', 'finbolt' ),
              'testimonials' => __( 'Testimonials', 'finbolt' ),
              'support'      => __( 'Support centre', 'finbolt' ),
              'login'        => __( 'Log in', 'finbolt' ),
              'register'     => __( 'Create account', 'finbolt' ),
            )
          );
          ?>
        </div>
      </div>
      <div>
        <h4><?php esc_html_e( 'Company', 'finbolt' ); ?></h4>
        <div class="footer__links">
          <?php
          finbolt_footer_links(
            'footer-company',
            array(
              'about'   => __( 'About', 'finbolt' ),
              'career'  => __( 'Career', 'finbolt' ),
              'blog'    => __( 'Blog', 'finbolt' ),
              'contact' => __( 'Contact us', 'finbolt' ),
            )
          );
          ?>
        </div>
      </div>
      <div>
        <h4><?php esc_html_e( 'Follow along', 'finbolt' ); ?></h4>
        <div class="social">
          <?php
          foreach ( $finbolt_socials as $finbolt_key => $finbolt_meta ) {
            $finbolt_url = get_theme_mod( $finbolt_key, '' );
            if ( ! $finbolt_url ) {
              continue;
            }
            printf(
              '<a href="%1$s" aria-label="%2$s"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%3$s" stroke="%4$s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%5$s</svg></a>',
              esc_url( $finbolt_url ),
              esc_attr( sprintf( /* translators: %s: network name. */ __( '%s profile', 'finbolt' ), $finbolt_meta[0] ) ),
              $finbolt_meta[2] ? 'currentColor' : 'none',
              $finbolt_meta[2] ? 'none' : 'currentColor',
              $finbolt_meta[1] // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static path data.
            );
          }
          ?>
        </div>
        <p class="footer__blurb" style="margin-top:16px">
          <?php if ( $finbolt_email ) : ?>
            <a href="<?php echo esc_url( 'mailto:' . $finbolt_email ); ?>"><?php echo esc_html( $finbolt_email ); ?></a><br>
          <?php endif; ?>
          <?php echo esc_html( $finbolt_phone ); ?>
        </p>
      </div>
    </div>
    <div class="footer__bar">
      <span><?php echo esc_html( get_theme_mod( 'finbolt_brand_name', get_bloginfo( 'name' ) ) ); ?></span>
      <span>
        <?php
        printf(
          /* translators: 1: year, 2: site name. */
          esc_html__( '&copy; %1$s %2$s. All rights reserved.', 'finbolt' ),
          esc_html( gmdate( 'Y' ) ),
          esc_html( get_bloginfo( 'name' ) )
        );
        ?>
      </span>
    </div>
  </footer>

</div>
<?php wp_footer(); ?>
</body>
</html>
