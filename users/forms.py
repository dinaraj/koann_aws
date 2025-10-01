from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'picture',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        labels = {
            'email': _("Adresse mail professionnelle"),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(help_text=('<a href="../password/">' + _("Changer le mot de passe") + '</a>'))

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'picture',
            'is_active',
            'is_staff',
            'is_superuser',
        )


class AccountSignupForm(SignupForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3)
    first_name = forms.CharField(label=_('Prénom'), max_length=255)
    last_name = forms.CharField(label=_('Nom'), max_length=255)

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['captcha'].label = ''
        self.fields['email'].label = _("Adresse mail")
        self.fields['password1'].help_text = _('Minimum 8 caractères')
        self.fields['password2'].label = _('Confirmer le mot de passe')

        self.fields['password1'].widget.attrs['class'] = 'toggle-password'
        self.fields['password2'].widget.attrs['class'] = 'toggle-password'

        del self.fields['email'].widget.attrs['placeholder']
        del self.fields['password1'].widget.attrs['placeholder']
        del self.fields['password2'].widget.attrs['placeholder']

    def save(self, request):
        user = super(AccountSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class AccountLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = _("Adresse mail")
        self.fields['password'].widget.attrs['class'] = 'toggle-password'
        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']

