# Permissions and Groups Setup

## Custom Permissions
Defined in `Book` model (`models.py`):
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

## Groups
Configured via Django Admin:
- **Viewers** → `can_view`
- **Editors** → `can_create`, `can_edit`
- **Admins** → all permissions

## Views
Each view in `views.py` uses `@permission_required` to enforce the right permission.
- `book_list` → requires `can_view`
- `add_book` → requires `can_create`
- `edit_book` → requires `can_edit`
- `delete_book` → requires `can_delete`

# HTTPS and Secure Redirects

## Security Settings in Django
- `SECURE_SSL_REDIRECT = True`: Forces HTTPS for all requests.
- `SECURE_HSTS_SECONDS = 31536000`: Enforces HSTS for 1 year.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Applies HSTS to subdomains.
- `SECURE_HSTS_PRELOAD = True`: Enables HSTS preload.
- `SESSION_COOKIE_SECURE = True`: Restricts cookies to HTTPS.
- `CSRF_COOKIE_SECURE = True`: Restricts CSRF cookie to HTTPS.
- `X_FRAME_OPTIONS = "DENY"`: Prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents MIME sniffing.
- `SECURE_BROWSER_XSS_FILTER = True`: Enables browser’s XSS filter.

## Deployment Notes
- SSL/TLS configured on web server (Nginx/Apache).
- All HTTP traffic redirected to HTTPS.
- Certificates installed via Let's Encrypt.

## Security Review
- All traffic is encrypted.
- Cookies are secure-only.
- HSTS prevents protocol downgrades.
- Headers protect against XSS and clickjacking.
- Future improvements: Use `django-secure` or `django-csp` for Content Security Policy.
