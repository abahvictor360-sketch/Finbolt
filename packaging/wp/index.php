<?php
/**
 * Blog index. Also the fallback template WordPress requires.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();

$finbolt_posts_page = (int) get_option( 'page_for_posts' );
$finbolt_title      = $finbolt_posts_page ? get_the_title( $finbolt_posts_page ) : __( 'Blog', 'finbolt' );
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php esc_html_e( 'Blog', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php echo esc_html( $finbolt_title ); ?></h1>
      <p><?php esc_html_e( 'Notes on money, fraud and getting paid, from the team running payments for ten thousand businesses.', 'finbolt' ); ?></p>
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php echo esc_html( $finbolt_title ); ?></span></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <?php if ( have_posts() ) : ?>
        <div class="grid grid--3">
          <?php
          while ( have_posts() ) :
            the_post();
            get_template_part( 'template-parts/post-card' );
          endwhile;
          ?>
        </div>
        <?php finbolt_pagination(); ?>
      <?php else : ?>
        <?php get_template_part( 'template-parts/content-none' ); ?>
      <?php endif; ?>
    </div>
  </section>
<?php
get_footer();
