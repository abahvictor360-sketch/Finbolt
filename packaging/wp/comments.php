<?php
/**
 * Comments.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

if ( post_password_required() ) {
	return;
}
?>
<div id="comments" class="comments">
  <?php if ( have_comments() ) : ?>
    <h2 class="comments__title">
      <?php
      $finbolt_count = get_comments_number();
      printf(
        esc_html( _n( '%s comment', '%s comments', $finbolt_count, 'finbolt' ) ),
        esc_html( number_format_i18n( $finbolt_count ) )
      );
      ?>
    </h2>

    <ol class="comment-list">
      <?php
      wp_list_comments(
        array(
          'style'      => 'ol',
          'short_ping' => true,
          'avatar_size' => 40,
        )
      );
      ?>
    </ol>

    <?php finbolt_pagination(); ?>

    <?php if ( ! comments_open() ) : ?>
      <p class="form__note"><?php esc_html_e( 'Comments are closed.', 'finbolt' ); ?></p>
    <?php endif; ?>
  <?php endif; ?>

  <?php
  comment_form(
    array(
      'class_submit'  => 'submit btn btn--primary',
      'title_reply'   => esc_html__( 'Leave a comment', 'finbolt' ),
    )
  );
  ?>
</div>
