<?php
/**
 * A single post.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

get_header();

while ( have_posts() ) :
  the_post();
  $finbolt_cats = get_the_category();
?>
  <section class="band pagehead">
    <div class="wrap">
      <span class="eyebrow eyebrow--onblue"><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg></i><?php echo ! empty( $finbolt_cats ) ? esc_html( $finbolt_cats[0]->name ) : esc_html__( 'Blog', 'finbolt' ); ?></span>
      <h1 style="margin-top:18px"><?php the_title(); ?></h1>
      
      <p class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'finbolt' ); ?></a> <span>/</span> <span><?php esc_html_e( 'Post', 'finbolt' ); ?></span></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <article id="post-<?php the_ID(); ?>" <?php post_class( 'entry reveal' ); ?>>
        <p class="entry__meta">
          <?php echo finbolt_icon( 'clock' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup. ?>
          <span><?php echo esc_html( get_the_date() ); ?></span>
          <span>&middot;</span>
          <span><?php echo esc_html( get_the_author() ); ?></span>
        </p>

        <?php if ( has_post_thumbnail() ) : ?>
          <div class="entry__thumb"><?php the_post_thumbnail( 'large' ); ?></div>
        <?php endif; ?>

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

        <?php if ( has_tag() ) : ?>
          <div class="entry__tags">
            <?php
            foreach ( get_the_tags() as $finbolt_tag ) {
              printf(
                '<a class="pill-tag" href="%1$s">%2$s</a>',
                esc_url( get_tag_link( $finbolt_tag->term_id ) ),
                esc_html( $finbolt_tag->name )
              );
            }
            ?>
          </div>
        <?php endif; ?>
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
