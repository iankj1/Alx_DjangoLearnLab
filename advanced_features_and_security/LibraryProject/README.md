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
