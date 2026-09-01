<?php
/**
 * Render the theme's templates against stubbed WordPress functions.
 *
 * Linting proves syntax; this proves the templates actually execute, that every
 * function they call exists, and that they emit the markup the design expects.
 * It is not a substitute for testing in WordPress, but it catches typos, missing
 * helpers and fatal errors before a buyer ever sees them.
 */

define( 'ABSPATH', __DIR__ . '/' );
$theme = $argv[1] ?? ( __DIR__ . '/../../dist/_theme' );
if ( ! is_dir( $theme ) ) {
	fwrite( STDERR, "usage: php render.php /path/to/theme\n" );
	exit( 2 );
}
define( 'THEME', realpath( $theme ) );

// --dump <dir> writes each rendered template to disk so the output can be
// opened in a browser and compared against the static template.
$dump = null;
$flag = array_search( '--dump', $argv, true );
if ( false !== $flag && isset( $argv[ $flag + 1 ] ) ) {
	$dump = $argv[ $flag + 1 ];
	@mkdir( $dump, 0777, true );
}

$GLOBALS['stub_posts'] = 1;   // one fake post for the loops
$GLOBALS['dump_mode'] = false;
// --elementor simulates the plugin being active; --takeover additionally has
// Elementor Theme Builder supplying the header, footer, single and archive.
$GLOBALS['elementor']  = in_array( '--elementor', $argv, true ) || in_array( '--takeover', $argv, true );
$GLOBALS['takeover']   = in_array( '--takeover', $argv, true );
$GLOBALS['is_builder'] = false;

/* ---- i18n + escaping ---------------------------------------------------- */
function __( $t, $d = null ) { return $t; }
function _x( $t, $c, $d = null ) { return $t; }
function _n( $s, $p, $n, $d = null ) { return $n == 1 ? $s : $p; }
function esc_html( $t ) { return htmlspecialchars( (string) $t, ENT_QUOTES ); }
function esc_attr( $t ) { return htmlspecialchars( (string) $t, ENT_QUOTES ); }
function esc_url( $u ) { return htmlspecialchars( (string) $u, ENT_QUOTES ); }
function esc_url_raw( $u ) { return $u; }
function esc_textarea( $t ) { return esc_html( $t ); }
function esc_html__( $t, $d = null ) { return esc_html( $t ); }
function esc_attr__( $t, $d = null ) { return esc_attr( $t ); }
function esc_html_e( $t, $d = null ) { echo esc_html( $t ); }
function esc_attr_e( $t, $d = null ) { echo esc_attr( $t ); }
function _e( $t, $d = null ) { echo esc_html( $t ); }
function wp_kses_post( $t ) { return $t; }
function wp_strip_all_tags( $t ) { return strip_tags( (string) $t ); }
function sanitize_text_field( $t ) { return trim( strip_tags( (string) $t ) ); }
function sanitize_email( $t ) { return $t; }
function sanitize_key( $t ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $t ) ); }
function sanitize_hex_color( $c ) { return preg_match( '/^#[0-9a-fA-F]{6}$/', (string) $c ) ? $c : null; }
function number_format_i18n( $n ) { return number_format( $n ); }
function untrailingslashit( $s ) { return rtrim( (string) $s, '/' ); }
function trailingslashit( $s ) { return untrailingslashit( $s ) . '/'; }
function wp_unique_id( $p = '' ) { static $i = 0; return $p . ++$i; }

/* ---- theme plumbing ----------------------------------------------------- */
function add_action( $h, $f, $p = 10, $a = 1 ) { $GLOBALS['actions'][ $h ][] = $f; }
function add_filter( $h, $f, $p = 10, $a = 1 ) { $GLOBALS['filters'][ $h ][] = $f; }
function add_theme_support( $f, $a = null ) { $GLOBALS['supports'][] = $f; }
function add_editor_style( $s ) {}
function register_nav_menus( $m ) { $GLOBALS['menus'] = $m; }
function register_sidebar( $a ) { $GLOBALS['sidebars'][] = $a['id']; }
function is_active_sidebar( $i ) { return false; }
function load_theme_textdomain( $d, $p ) { return true; }
function get_template_directory() { return THEME; }
function get_template_directory_uri() {
	// When dumping, assets sit beside the rendered file.
	return $GLOBALS['dump_mode'] ? '.' : 'https://example.test/wp-content/themes/finbolt';
}
function get_stylesheet_uri() { return get_template_directory_uri() . '/style.css'; }
function wp_enqueue_style( ...$a ) {
	$GLOBALS['styles'][] = $a[0];
	if ( ! empty( $a[1] ) ) {
		$GLOBALS['style_src'][ $a[0] ] = $a[1];
	}
}
function wp_enqueue_script( ...$a ) {
	$GLOBALS['scripts'][] = $a[0];
	if ( ! empty( $a[1] ) ) {
		$GLOBALS['script_src'][ $a[0] ] = $a[1];
	}
}
function wp_add_inline_style( $h, $css ) { $GLOBALS['inline'][] = $css; }
function wp_localize_script( $h, $n, $d ) { $GLOBALS['localized'][ $n ] = $d; }

/**
 * Emit what WordPress would print for the enqueued assets, so a dumped page is
 * actually renderable and can be compared with the static template.
 */
function wp_head() {
	echo '<title>' . esc_html( get_bloginfo( 'name' ) ) . "</title>\n";
	foreach ( $GLOBALS['style_src'] ?? array() as $handle => $src ) {
		printf( "<link rel=\"stylesheet\" id=\"%s\" href=\"%s\">\n", esc_attr( $handle ), esc_url( $src ) );
	}
	foreach ( $GLOBALS['inline'] ?? array() as $css ) {
		printf( "<style>%s</style>\n", $css );
	}
}
function wp_footer() {
	foreach ( $GLOBALS['localized'] ?? array() as $name => $data ) {
		printf( "<script>var %s = %s;</script>\n", $name, wp_json_encode( $data ) );
	}
	foreach ( $GLOBALS['script_src'] ?? array() as $handle => $src ) {
		printf( "<script src=\"%s\" id=\"%s\"></script>\n", esc_url( $src ), esc_attr( $handle ) );
	}
}
function wp_json_encode( $d ) { return json_encode( $d ); }
function wp_body_open() {}
function language_attributes() { echo 'lang="en-US"'; }
function body_class( $c = '' ) { echo 'class="finbolt"'; }
function post_class( $c = '' ) { echo 'class="' . esc_attr( is_array( $c ) ? implode( ' ', $c ) : $c ) . '"'; }
function bloginfo( $k ) { echo get_bloginfo( $k ); }
function get_bloginfo( $k = 'name' ) {
	return 'charset' === $k ? 'UTF-8' : 'Finbolt Demo';
}
function home_url( $p = '/' ) { return 'https://example.test' . $p; }
function get_theme_mod( $k, $d = false ) { return $d; }
function has_custom_logo() { return false; }
function has_nav_menu( $l ) { return false; }
function wp_nav_menu( $a ) {}
function get_pages( $a = array() ) { return array(); }
function get_page_by_path( $p ) { return null; }
function get_permalink( $p = 0 ) { return 'https://example.test/sample/'; }
function get_option( $k, $d = false ) { return 'page_for_posts' === $k ? 0 : $d; }
function get_search_form( $a = array() ) { include THEME . '/searchform.php'; }
function get_search_query() { return 'settlement'; }
function is_front_page() { return true; }
function is_singular() { return false; }
function is_admin() { return false; }
function did_action( $h ) {
	return ( 'elementor/loaded' === $h && $GLOBALS['elementor'] ) ? 1 : 0;
}
function is_page_template( $t = '' ) { return $GLOBALS['is_builder'] ?? false; }
function wp_add_inline_script( $h, $js, $pos = 'after' ) { $GLOBALS['inline_js'][] = $js; }
function get_queried_object_id() { return 0; }
function comments_open() { return false; }
function get_comments_number() { return 0; }
function comments_template() {}
function post_password_required() { return false; }
function have_comments() { return false; }
function wp_list_comments( $a ) {}
function comment_form( $a = array() ) {}
function the_posts_pagination( $a = array() ) { echo '<nav class="pagination"></nav>'; }
function wp_link_pages( $a = array() ) {}
function get_template_part( $slug, $name = null ) {
	$file = THEME . '/' . $slug . ( $name ? "-$name" : '' ) . '.php';
	if ( ! file_exists( $file ) ) {
		throw new RuntimeException( "missing template part: $slug" );
	}
	include $file;
}
function get_header() { include THEME . '/header.php'; }
function get_footer() { include THEME . '/footer.php'; }

/* ---- loop stubs --------------------------------------------------------- */
function have_posts() { return $GLOBALS['stub_posts']-- > 0; }
function the_post() {}
function the_ID() { echo '1'; }
function the_title() { echo 'A sample post title'; }
function get_the_title( $p = 0 ) { return 'A sample post title'; }
function the_permalink() { echo esc_url( get_permalink() ); }
function the_content() { echo '<p>Sample content.</p>'; }
function get_the_excerpt() { return 'A short sample excerpt for the card.'; }
function get_the_date() { return '12 August 2026'; }
function get_the_author() { return 'John Clayton'; }
function get_the_category() { return array( (object) array( 'name' => 'Product' ) ); }
function has_post_thumbnail() { return false; }
function the_post_thumbnail( $s = 'large' ) {}
function wp_get_attachment_image( ...$a ) { return ''; }
function has_tag() { return false; }
function get_the_tags() { return array(); }
function get_tag_link( $id ) { return home_url( '/tag/sample/' ); }
function get_the_archive_title() { return 'Category: Product'; }
function the_archive_description( $b = '', $a = '' ) {}

$GLOBALS['dump_mode'] = (bool) $dump;

if ( $GLOBALS['elementor'] ) {
	// Elementor's public helper. Returns true when a Theme Builder template
	// covers this location, in which case the theme must not render its own.
	function elementor_theme_do_location( $location ) {
		if ( ! $GLOBALS['takeover'] ) {
			return false;
		}
		echo "<!-- elementor:$location -->";
		return true;
	}
}

/* ---- core classes ------------------------------------------------------- */
class Walker {}
class Walker_Nav_Menu extends Walker {}
class WP_Customize_Manager {
	public function add_panel( ...$a ) {}
	public function add_section( ...$a ) {}
	public function add_setting( ...$a ) { $GLOBALS['settings'][] = is_string( $a[0] ) ? $a[0] : '?'; }
	public function add_control( ...$a ) { $GLOBALS['controls'][] = is_string( $a[0] ) ? $a[0] : get_class( $a[0] ); }
	public function get_setting( $id ) { return (object) array( 'transport' => 'refresh' ); }
}
class WP_Customize_Color_Control {
	public function __construct( ...$a ) {}
}

/* ---- run ---------------------------------------------------------------- */
require THEME . '/functions.php';

// Fire the hooks the theme registered, as WordPress would.
foreach ( array( 'after_setup_theme', 'wp_enqueue_scripts', 'widgets_init' ) as $hook ) {
	foreach ( $GLOBALS['actions'][ $hook ] ?? array() as $fn ) {
		$fn();
	}
}

$templates = array_merge(
	array( 'front-page.php', 'index.php', 'single.php', 'page.php', 'archive.php', 'search.php', '404.php' ),
	array_map(
		function ( $p ) { return 'page-templates/' . basename( $p ); },
		glob( THEME . '/page-templates/*.php' )
	)
);

$fail = 0;
foreach ( $templates as $tpl ) {
	$GLOBALS['stub_posts'] = 1;
	ob_start();
	try {
		include THEME . '/' . $tpl;
		$html = ob_get_clean();
	} catch ( Throwable $e ) {
		ob_end_clean();
		printf( "  FAIL  %-34s %s\n", $tpl, $e->getMessage() );
		$fail++;
		continue;
	}

	$takeover = $GLOBALS['takeover'];
	$checks = array(
		'doctype'      => stripos( $html, '<!doctype html>' ) === 0,
		'frame'        => strpos( $html, 'class="frame"' ) !== false,
		'header'       => $takeover
			? ( strpos( $html, 'class="header"' ) === false
				&& strpos( $html, '<!-- elementor:header -->' ) !== false )
			: strpos( $html, 'class="header"' ) !== false,
		'main closed'  => strpos( $html, '</main>' ) !== false,
		'footer'       => $takeover
			? ( strpos( $html, 'class="footer"' ) === false
				&& strpos( $html, '<!-- elementor:footer -->' ) !== false )
			: strpos( $html, 'class="footer"' ) !== false,
		'closed html'  => strpos( $html, '</html>' ) !== false,
		'no raw php'   => strpos( $html, '<?php' ) === false,
		'no .html link' => ! preg_match( '/href="[a-z0-9\-]+\.html"/', $html ),
		'css linked'   => strpos( $html, 'assets/css/style.css' ) !== false,
		'js linked'    => strpos( $html, 'assets/js/main.js' ) !== false,
	);
	$bad = array_keys( array_filter( $checks, function ( $v ) { return ! $v; } ) );
	if ( $bad ) {
		printf( "  FAIL  %-34s %s\n", $tpl, implode( ', ', $bad ) );
		$fail++;
	} else {
		printf( "  ok    %-34s %6d bytes\n", $tpl, strlen( $html ) );
	}

	if ( $dump ) {
		$name = str_replace( array( 'page-templates/', '.php' ), array( 'tpl-', '' ), $tpl );
		file_put_contents( rtrim( $dump, '/' ) . '/' . $name . '.html', $html );
	}
}

// The customizer panel is a big surface area; run it too.
foreach ( $GLOBALS['actions']['customize_register'] ?? array() as $fn ) {
	$fn( new WP_Customize_Manager() );
}

echo "\n";
printf( "customizer settings : %d settings, %d controls\n",
	count( $GLOBALS['settings'] ?? array() ), count( $GLOBALS['controls'] ?? array() ) );
printf( "supports registered : %d\n", count( $GLOBALS['supports'] ?? array() ) );
printf( "menu locations      : %s\n", implode( ', ', array_keys( $GLOBALS['menus'] ?? array() ) ) );
printf( "sidebars            : %s\n", implode( ', ', $GLOBALS['sidebars'] ?? array() ) );
printf( "styles enqueued     : %s\n", implode( ', ', $GLOBALS['styles'] ?? array() ) );
printf( "scripts enqueued    : %s\n", implode( ', ', $GLOBALS['scripts'] ?? array() ) );
printf( "localized to JS     : %s\n", json_encode( $GLOBALS['localized'] ?? array() ) );
printf( "elementor active    : %s%s\n",
	$GLOBALS['elementor'] ? 'yes' : 'no',
	$GLOBALS['takeover'] ? ' (theme builder supplying header/footer/single/archive)' : '' );

exit( $fail ? 1 : 0 );
