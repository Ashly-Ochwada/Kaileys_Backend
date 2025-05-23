from django.contrib import admin
from .models import Organization, Course, AccessCode, Trainee, AccessGrant

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'course', 'organization', 'created_at', 'expires_at')
    list_filter = ('organization', 'course')
    search_fields = ('code',)

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'organization')
    search_fields = ('phone_number',)

@admin.register(AccessGrant)
class AccessGrantAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'course', 'access_granted_at', 'expires_at')
    list_filter = ('course',)
