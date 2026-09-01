<?php
/**
 * Search results.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php esc_html_e( 'Search', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php
      printf(
        /* translators: %s: search query. */
        esc_html__( 'Results for %s', 'finbolt' ),
        '&ldquo;' . esc_html( get_search_query() ) . '&rdquo;'
      );
      ?></h1>
      
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php esc_html_e( 'Search', 'finbolt' ); ?></span></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div style="max-width:560px;margin:0 auto 40px"><?php get_search_form(); ?></div>
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
