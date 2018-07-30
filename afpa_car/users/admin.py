from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, PrivateData

class ProfileInline(admin.StackedInline):
    model = PrivateData
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email','username', 'is_active', 'is_admin',  'is_staff', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal infos', {'fields': ('first_name', 'last_name', 'avatar', 'trainee', 'driver_license', 'car_owner')}),
        ('Preferences', {'fields': ('smoker', 'talker', 'music')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
        
    )
    add_fieldsets = (
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username',  
                        'password1', 'password2',)}
        ),
        ('Optional Fields', {
            'classes': ('wide',),
            'fields': ('avatar', 'driver_license', 'trainee', 'car_owner','smoker', 'talker', 'music')}
        ),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_admin',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)


# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)