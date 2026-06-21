from django.contrib import admin
from .models import Organization, Course, Trainee


class TraineeInline(admin.TabularInline):
    model = Trainee
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Organization model.
    """
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_per_page = 25
    inlines = [TraineeInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    """
    list_display = ('name', 'access_code', 'access_code_expires_at')
    search_fields = ('name', 'access_code')
    list_filter = ('access_code_expires_at',)
    list_per_page = 25


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trainee model.
    """
    list_display = ('full_name', 'phone_number', 'organization')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('organization',)
    list_per_page = 25