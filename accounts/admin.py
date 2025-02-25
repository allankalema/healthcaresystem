from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Doctor, Specialization

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_doctor', 'is_patient', 'is_hospital', 'is_staff', 'is_superuser')
    list_filter = ('is_doctor', 'is_patient', 'is_hospital', 'is_staff', 'is_superuser', 'marital_status')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nin', 'contact')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (_("Personal Information"), {'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'nin', 'marital_status', 'contact')}),
        (_("Permissions"), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor', 'is_patient', 'is_hospital', 'groups', 'user_permissions')}),
        (_("Important Dates"), {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (_("Create New User"), {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_doctor', 'is_patient', 'is_hospital'),
        }),
    )

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'education_level', 'rank', 'display_specializations')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    list_filter = ('education_level', 'rank', 'specializations')
    filter_horizontal = ('specializations',)

    def display_specializations(self, obj):
        return ", ".join([s.name for s in obj.specializations.all()])
    display_specializations.short_description = "Specializations"

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specialization, SpecializationAdmin)
