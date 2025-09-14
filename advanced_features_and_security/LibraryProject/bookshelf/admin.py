from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    list_display = ["username", "email", "date_of_birth", "is_staff", "is_active"]

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns visible in the list view
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")
