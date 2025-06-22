from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    NewUser, UserDetails, CountryList, Permissions,
    UserRoles, RolePermissions, Tokens, Roles
)
from django.contrib.sessions.models import Session
from django.utils.timezone import localtime

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'ip_address', 'expire_date')
    readonly_fields = ('session_key', 'user', 'ip_address', 'expire_date')
    
    def user(self, obj):
        data = obj.get_decoded()
        user_id = data.get('_auth_user_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

    def ip_address(self, obj):
        # If you store IP in session, extract it here.
        data = obj.get_decoded()
        return data.get('ip')  # Modify this as per your implementation
    
    def expire_date(self, obj):
        return localtime(obj.expire_date)


class CustomUserAdmin(UserAdmin):
    model = NewUser
    list_display = ('email', 'source', 'is_staff', 'is_active', 'is_verified', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('created_at', 'last_modified', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'source')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'last_modified', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified')
        }),
    )

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('role_id', 'name')

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'middle_name', 'last_name', 'country_id')
    search_fields = ('first_name', 'last_name', 'country_id')


@admin.register(CountryList)
class CountryListAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'name')
    search_fields = ('name',)


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('permission_id', 'name')
    search_fields = ('name',)


@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role_id')


@admin.register(RolePermissions)
class RolePermissionsAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'permission_id')


@admin.register(Tokens)
class TokensAdmin(admin.ModelAdmin):
    list_display = ('token_id', 'user', 'token_hash', 'expires_at', 'created_at')
    search_fields = ('user__email', 'token_hash')
    readonly_fields = ('created_at',)


# Register the custom user admin
admin.site.register(NewUser, CustomUserAdmin)
