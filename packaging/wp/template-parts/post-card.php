<?php
/**
 * One post in the blog grid.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

$finbolt_cats = get_the_category();
?>
<article id="post-<?php the_ID(); ?>" <?php post_class( 'post reveal reveal--scale' ); ?>>
  <a class="post__thumb" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1">
    <?php
    if ( has_post_thumbnail() ) {
      the_post_thumbnail( 'large' );
    } else {
      echo finbolt_icon( 'chart' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup.
    }
    ?>
  </a>
  <div class="post__body">
    <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
    <p><?php echo esc_html( get_the_excerpt() ); ?></p>
    <p class="post__meta">
      <?php if ( ! empty( $finbolt_cats ) ) : ?>
        <span class="pill-tag"><?php echo esc_html( $finbolt_cats[0]->name ); ?></span>
      <?php endif; ?>
      <span><?php echo esc_html( get_the_date() ); ?></span>
    </p>
  </div>
</article>
