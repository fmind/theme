# Fmind for WordPress

Fmind light admin color scheme for WordPress.

Format: [wp_admin_css_color()](https://developer.wordpress.org/reference/functions/wp_admin_css_color/) · [core admin color selectors](https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/css/colors/_admin.scss)

## Installation

Copy `fmind.css` into your theme, register it with `wp_admin_css_color()` in the theme's `functions.php` (or from a custom plugin with its own URL), then select Fmind under Users → Profile → Admin Color Scheme:

```php
add_action( 'admin_init', function () {
    wp_admin_css_color( 'fmind', 'Fmind', get_stylesheet_directory_uri() . '/fmind.css', array( '#ffffff', '#f1f3f4', '#174ea6', '#d2e3fc' ) );
} );
```
