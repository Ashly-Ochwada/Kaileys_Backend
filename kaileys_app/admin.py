from django.contrib import admin
from .models import Organization, Course, AccessCode, Trainee, AccessGrant

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Organization model.
    Customizes the list view, search functionality, and pagination.
    """
    # Fields to display in the list view
    list_display = ('name', 'country')
    
    # Fields to enable search functionality
    search_fields = ('name',)
    
    # Number of items to display per page in the list view
    list_per_page = 25

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    Customizes the list view, search functionality, and pagination.
    """
    # Fields to display in the list view
    list_display = ('name',)
    
    # Fields to enable search functionality
    search_fields = ('name',)
    
    # Number of items to display per page in the list view
    list_per_page = 25

@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AccessCode model.
    Customizes the list view, filters, search functionality, read-only fields, and pagination.
    """
    # Fields to display in the list view
    list_display = ('code', 'course', 'organization', 'created_at', 'expires_at')
    
    # Filters to enable in the sidebar
    list_filter = ('organization', 'course', 'created_at', 'expires_at')
    
    # Fields to enable search functionality
    search_fields = ('code',)
    
    # Fields that are read-only in the admin (code is auto-generated)
    readonly_fields = ('code',)
    
    # Number of items to display per page in the list view
    list_per_page = 25

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trainee model.
    Customizes the list view, search functionality, and pagination.
    """
    # Fields to display in the list view
    list_display = ('phone_number', 'organization')
    
    # Fields to enable search functionality
    search_fields = ('phone_number',)
    
    # Number of items to display per page in the list view
    list_per_page = 25

@admin.register(AccessGrant)
class AccessGrantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AccessGrant model.
    Customizes the list view, filters, and pagination.
    """
    # Fields to display in the list view
    list_display = ('trainee', 'course', 'access_granted_at', 'expires_at')
    
    # Filters to enable in the sidebar
    list_filter = ('course', 'access_granted_at', 'expires_at')
    
    # Number of items to display per page in the list view
    list_per_page = 25