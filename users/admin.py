from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.sessions.models import Session
from .models import Profile, Country, City, UserAccount, Project


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'updated_at', 'last_login')
    list_filter = ('email', 'is_superuser')
    search_fields = ('email', 'is_superuser', 'last_name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'features', 'github_link', 'demo_link', 'show', 'date_published', 'created_at']
    prepopulated_fields = {'slug': ['name']}


admin.site.site_header = 'My Portfolio Website'
admin.site.register(Session, SessionAdmin)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(UserAccount, UserAccountAdmin)