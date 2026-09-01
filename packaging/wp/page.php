<?php
/**
 * A standard page, for anything the buyer adds beyond the shipped templates.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();

while ( have_posts() ) :
  the_post();
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php esc_html_e( 'Finbolt', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php the_title(); ?></h1>
      
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php the_title(); ?></span></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <article id="post-<?php the_ID(); ?>" <?php post_class( 'entry reveal' ); ?>>
        <div class="entry__content">
          <?php
          the_content();

          wp_link_pages(
            array(
              'before' => '<nav class="pagination">',
              'after'  => '</nav>',
            )
          );
          ?>
        </div>
      </article>

      <?php
      if ( comments_open() || get_comments_number() ) {
        comments_template();
      }
      ?>
    </div>
  </section>
<?php
endwhile;

get_footer();
