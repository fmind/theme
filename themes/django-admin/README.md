# Django Admin

Fmind theme for [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/).

Format: [Django admin theming](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#theming-support) · [base.css](https://github.com/django/django/blob/main/django/contrib/admin/static/admin/css/base.css)

## Install

Serve `fmind.css` as a static file, override `admin/base_site.html`, and link it in the `extrastyle` block with `{{ block.super }}`. Django's dark-mode toggle can override it; select the light theme.
