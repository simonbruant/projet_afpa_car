from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, PrivateData, UserProfile

class PrivateDataInline(admin.StackedInline):
    model = PrivateData
    can_delete = False
    verbose_name_plural = "Private Data"
    fk_name = 'user'

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (PrivateDataInline, UserProfileInline )
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email','username', 'is_active', 'is_admin',  'is_staff', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'is_staff')
    readonly_fields = ('date_joined', 'confirm', 'confirmation_date')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal infos', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),   
        ('Other infos', {'fields': ('date_joined', 'confirm', 'confirmation_date')}),   
    )
    add_fieldsets = (
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username',  
                        'password1', 'password2',)}
        ),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_admin',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('-is_admin', '-date_joined',)
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)