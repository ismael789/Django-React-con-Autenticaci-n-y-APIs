from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, User

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)


@admin.register(User)
class StoreUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'carrera', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username', 'first_name', 'last_name', 'carrera')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'carrera')}),
    )
    search_fields = ('email', 'first_name', 'last_name', 'carrera')
