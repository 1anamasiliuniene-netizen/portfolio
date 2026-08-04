# Deployment

This Django project is configured for environment-based deployment.

## Required Environment Variables

- `DJANGO_DEBUG=false`
- `DJANGO_SECRET_KEY`: a long random secret value
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames, for example `www.example.com,example.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated HTTPS origins, for example `https://www.example.com,https://example.com`

Optional security overrides:

- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_USE_X_FORWARDED_PROTO`: set to `true` when the deployment host terminates HTTPS before forwarding requests to Django
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`

## Build Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Collect static assets:

```bash
python manage.py collectstatic --noinput
```

## Start Command

```bash
gunicorn config.wsgi:application
```

## Uploaded Files

Admin-uploaded images, resumes, and certificates are stored in `media/`.
In production, make sure your host provides persistent media storage or a persistent disk.
