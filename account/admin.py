from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'company', 'position', 'phone_number']
    list_display_links = ['user']
    list_editable = ['phone_number', 'photo']
    search_fields = ['user__email', 'user__username', 'user__first_name', 
    'user__last_name', 'phone_number']
    list_filter = ['user__is_active', 'user__is_staff']
    fieldsets = (
        ('Profile', {
            'fields': (
                (
                    'user',
                    'photo',
                ),
            ),
        }),
        ('Extra info', {
            'fields': (
                ('company', 'position'),
                'phone_number',
            ),
        })
    )

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)