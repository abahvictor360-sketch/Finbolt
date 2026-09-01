<?php
/**
 * Category, tag, author and date archives.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php esc_html_e( 'Archive', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php echo esc_html( wp_strip_all_tags( get_the_archive_title() ) ); ?></h1>
      <?php the_archive_description( '<p>', '</p>' ); ?>
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php esc_html_e( 'Archive', 'finbolt' ); ?></span></p>
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
