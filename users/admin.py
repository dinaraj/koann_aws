from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import UserChangeForm, UserCreationForm


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = [
        '__str__',
        'email',
        'id',
        'is_staff',
        'is_superuser',
    ]
    list_display_links = ('__str__', 'email',)
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('first_name', 'last_name', 'phone', 'picture')}),
        (
            _('Autorisations (permissions)'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'mail_incidents',
                    'groups'
                )
            }
        ),
        (_("Dates clés"), {"fields": ("last_login", "created_at")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',),
        }),
    )
    ordering = ('-date_joined',)
    search_fields = ['email', 'first_name', 'last_name', 'id']

    def groups_list(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return " ".join(groups)

    groups_list.short_description = "Groupes"
