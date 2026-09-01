<?php
/**
 * Customizer panel: brand, colours, calls to action and footer details.
 *
 * @package Finbolt
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register the theme's settings.
 *
 * @param WP_Customize_Manager $wp_customize Customizer instance.
 */
function finbolt_customize_register( $wp_customize ) {

	$wp_customize->get_setting( 'blogname' )->transport        = 'postMessage';
	$wp_customize->get_setting( 'blogdescription' )->transport = 'postMessage';

	$wp_customize->add_panel(
		'finbolt_panel',
		array(
			'title'    => __( 'Finbolt theme', 'finbolt' ),
			'priority' => 20,
		)
	);

	/* ---- Brand ---------------------------------------------------------- */
	$wp_customize->add_section(
		'finbolt_brand',
		array(
			'title' => __( 'Brand', 'finbolt' ),
			'panel' => 'finbolt_panel',
		)
	);

	$wp_customize->add_setting(
		'finbolt_brand_name',
		array(
			'default'           => get_bloginfo( 'name' ),
			'sanitize_callback' => 'sanitize_text_field',
			'transport'         => 'postMessage',
		)
	);
	$wp_customize->add_control(
		'finbolt_brand_name',
		array(
			'label'       => __( 'Wordmark text', 'finbolt' ),
			'description' => __( 'Shown beside the logo mark. Defaults to the site title.', 'finbolt' ),
			'section'     => 'finbolt_brand',
			'type'        => 'text',
		)
	);

	/* ---- Colours -------------------------------------------------------- */
	$wp_customize->add_section(
		'finbolt_colors',
		array(
			'title'       => __( 'Colours', 'finbolt' ),
			'description' => __( 'These feed the design tokens, so every page follows.', 'finbolt' ),
			'panel'       => 'finbolt_panel',
		)
	);

	foreach ( finbolt_color_settings() as $key => $meta ) {
		$wp_customize->add_setting(
			$key,
			array(
				'default'           => $meta['default'],
				'sanitize_callback' => 'sanitize_hex_color',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				$key,
				array(
					'label'       => $meta['label'],
					'description' => $meta['description'],
					'section'     => 'finbolt_colors',
				)
			)
		);
	}

	/* ---- Calls to action ------------------------------------------------ */
	$wp_customize->add_section(
		'finbolt_cta',
		array(
			'title'       => __( 'Buttons and sign-in', 'finbolt' ),
			'description' => __( 'Leave a field empty to use the theme\'s own register and login page templates.', 'finbolt' ),
			'panel'       => 'finbolt_panel',
		)
	);

	$wp_customize->add_setting(
		'finbolt_cta_label',
		array(
			'default'           => __( 'Get started', 'finbolt' ),
			'sanitize_callback' => 'sanitize_text_field',
			'transport'         => 'postMessage',
		)
	);
	$wp_customize->add_control(
		'finbolt_cta_label',
		array(
			'label'   => __( 'Button label', 'finbolt' ),
			'section' => 'finbolt_cta',
			'type'    => 'text',
		)
	);

	$wp_customize->add_setting(
		'finbolt_cta_url',
		array(
			'default'           => '',
			'sanitize_callback' => 'esc_url_raw',
		)
	);
	$wp_customize->add_control(
		'finbolt_cta_url',
		array(
			'label'       => __( 'Button link', 'finbolt' ),
			'description' => __( 'Point this at your own sign-up flow, or at wp-login.php?action=register.', 'finbolt' ),
			'section'     => 'finbolt_cta',
			'type'        => 'url',
		)
	);

	$wp_customize->add_setting(
		'finbolt_login_url',
		array(
			'default'           => '',
			'sanitize_callback' => 'esc_url_raw',
		)
	);
	$wp_customize->add_control(
		'finbolt_login_url',
		array(
			'label'   => __( 'Log in link', 'finbolt' ),
			'section' => 'finbolt_cta',
			'type'    => 'url',
		)
	);

	/* ---- Footer --------------------------------------------------------- */
	$wp_customize->add_section(
		'finbolt_footer',
		array(
			'title' => __( 'Footer', 'finbolt' ),
			'panel' => 'finbolt_panel',
		)
	);

	$wp_customize->add_setting(
		'finbolt_footer_blurb',
		array(
			'default'           => __( 'Finbolt is built on one idea: getting paid should be the simplest part of running a business.', 'finbolt' ),
			'sanitize_callback' => 'wp_kses_post',
			'transport'         => 'postMessage',
		)
	);
	$wp_customize->add_control(
		'finbolt_footer_blurb',
		array(
			'label'   => __( 'Footer paragraph', 'finbolt' ),
			'section' => 'finbolt_footer',
			'type'    => 'textarea',
		)
	);

	$text_fields = array(
		'finbolt_email'    => array( __( 'Contact email', 'finbolt' ), 'hello@finbolt.com', 'sanitize_email' ),
		'finbolt_phone'    => array( __( 'Phone', 'finbolt' ), '+234 700 346 6538', 'sanitize_text_field' ),
		'finbolt_social_x' => array( __( 'X / Twitter URL', 'finbolt' ), '', 'esc_url_raw' ),
		'finbolt_social_in' => array( __( 'LinkedIn URL', 'finbolt' ), '', 'esc_url_raw' ),
		'finbolt_social_fb' => array( __( 'Facebook URL', 'finbolt' ), '', 'esc_url_raw' ),
		'finbolt_social_ig' => array( __( 'Instagram URL', 'finbolt' ), '', 'esc_url_raw' ),
	);
	foreach ( $text_fields as $key => $field ) {
		$wp_customize->add_setting(
			$key,
			array(
				'default'           => $field[1],
				'sanitize_callback' => $field[2],
			)
		);
		$wp_customize->add_control(
			$key,
			array(
				'label'   => $field[0],
				'section' => 'finbolt_footer',
				'type'    => 'esc_url_raw' === $field[2] ? 'url' : 'text',
			)
		);
	}
}
add_action( 'customize_register', 'finbolt_customize_register' );

/**
 * The colour settings and the tokens they drive.
 *
 * @return array
 */
function finbolt_color_settings() {
	return array(
		'finbolt_color_blue'      => array(
			'default'     => '#1B6DF0',
			'token'       => '--blue',
			'label'       => __( 'Primary blue', 'finbolt' ),
			'description' => __( 'Buttons, links and accent words.', 'finbolt' ),
		),
		'finbolt_color_blue_deep' => array(
			'default'     => '#0B45C4',
			'token'       => '--blue-deep',
			'label'       => __( 'Deep blue', 'finbolt' ),
			'description' => __( 'Bottom of the gradient band and small text on tinted pills.', 'finbolt' ),
		),
		'finbolt_color_ink'       => array(
			'default'     => '#0B1220',
			'token'       => '--ink',
			'label'       => __( 'Heading ink', 'finbolt' ),
			'description' => __( 'Headings and strong text.', 'finbolt' ),
		),
	);
}

/**
 * Build the inline custom-property overrides, emitting only real changes.
 *
 * @return string
 */
function finbolt_color_overrides() {
	$rules = '';

	foreach ( finbolt_color_settings() as $key => $meta ) {
		$value = get_theme_mod( $key, $meta['default'] );
		if ( ! $value || strtolower( $value ) === strtolower( $meta['default'] ) ) {
			continue;
		}
		$clean = sanitize_hex_color( $value );
		if ( $clean ) {
			$rules .= sprintf( '%s:%s;', $meta['token'], $clean );
		}
	}

	return $rules ? ':root{' . $rules . '}' : '';
}
