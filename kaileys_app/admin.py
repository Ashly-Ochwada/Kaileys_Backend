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
    Enhances usability by showing key fields, enabling filters and search, 
    and displaying whether the access code is still valid.
    """

    # Fields to display in the list view of the admin
    list_display = ('code', 'course', 'organization', 'created_at', 'expires_at', 'is_valid')

    # Sidebar filters for narrowing down entries
    list_filter = ('organization', 'course', 'created_at', 'expires_at')

    # Searchable fields (useful when looking for a specific code)
    search_fields = ('code',)

    # Prevent editing of auto-generated code in the admin form
    readonly_fields = ('code',)

    # Pagination: number of entries per page
    list_per_page = 25

    # Custom method to display whether the access code is still valid
    def is_valid(self, obj):
        return obj.is_valid  # uses the @property on the model

    # Display as a boolean (checkmark) in the admin list view
    is_valid.boolean = True

    # Custom column header name
    is_valid.short_description = "Valid?"


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