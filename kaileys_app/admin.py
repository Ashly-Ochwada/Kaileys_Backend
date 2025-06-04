from django.contrib import admin
from .models import Organization, Course, Trainee, AccessGrant


class TraineeInline(admin.TabularInline):
    model = Trainee
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Organization model.
    Customizes the list view, search functionality, and pagination.
    """
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_per_page = 25
    inlines = [TraineeInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    Customizes the list view, search functionality, and pagination.
    """
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 25

class AccessGrantInline(admin.TabularInline):
    model = AccessGrant
    extra = 0

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trainee model.
    Customizes the list view, search functionality, and pagination.
    """
    list_display = ('phone_number', 'organization')
    search_fields = ('phone_number',)
    list_per_page = 25
    inlines = [AccessGrantInline]

@admin.register(AccessGrant)
class AccessGrantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AccessGrant model.
    Customizes the list view, filters, and pagination.
    """
    list_display = ('trainee', 'course', 'access_granted_at', 'expires_at')
    list_filter = ('course', 'access_granted_at', 'expires_at')
    list_per_page = 25
