<?php
/**
 * Opens every page: the card frame, the header and the drawer.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="profile" href="https://gmpg.org/xfn/11">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', 'finbolt' ); ?></a>
<div class="frame">
  <header class="header">
    <div class="wrap header__inner">
      <?php finbolt_brand(); ?>
      <nav class="nav" aria-label="<?php esc_attr_e( 'Primary', 'finbolt' ); ?>">
        <?php finbolt_nav( 'primary' ); ?>
      </nav>
      <a class="header__login" href="<?php echo esc_url( finbolt_login_url() ); ?>"><?php esc_html_e( 'Log in', 'finbolt' ); ?></a>
      <a class="header__cta" href="<?php echo esc_url( finbolt_cta_url() ); ?>"><?php
        echo esc_html( get_theme_mod( 'finbolt_cta_label', __( 'Get started', 'finbolt' ) ) );
      ?><span class="dot"><?php echo finbolt_icon( 'arrow' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup. ?></span></a>
      <button class="burger" data-drawer-open aria-label="<?php esc_attr_e( 'Open menu', 'finbolt' ); ?>">
        <span class="burger__bars"><i></i><i></i><i></i></span><?php esc_html_e( 'Menu', 'finbolt' ); ?>
      </button>
    </div>
  </header>

  <div class="drawer" data-drawer data-open="false" role="dialog" aria-modal="true" aria-label="<?php esc_attr_e( 'Menu', 'finbolt' ); ?>">
    <div class="drawer__panel">
      <div class="drawer__head">
        <?php finbolt_brand(); ?>
        <button class="drawer__close" data-drawer-close aria-label="<?php esc_attr_e( 'Close menu', 'finbolt' ); ?>">&times;</button>
      </div>
      <nav aria-label="<?php esc_attr_e( 'Mobile', 'finbolt' ); ?>">
        <?php finbolt_nav( 'primary' ); ?>
      </nav>
      <a class="btn btn--primary" href="<?php echo esc_url( finbolt_cta_url() ); ?>"><?php
        echo esc_html( get_theme_mod( 'finbolt_cta_label', __( 'Get started', 'finbolt' ) ) );
      ?><?php echo finbolt_icon( 'arrow' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static markup. ?></a>
      <a class="btn btn--ghost" href="<?php echo esc_url( finbolt_login_url() ); ?>" style="width:100%;justify-content:center;margin-top:10px"><?php esc_html_e( 'Log in', 'finbolt' ); ?></a>
    </div>
  </div>

  <main id="content">
