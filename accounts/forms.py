from django import forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


class CustomForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("رمز های عبور همخوانی ندارند"),
    }
    email = forms.EmailField(required=True, label=("ایمیل"))
    username = forms.CharField(label=("نام کاربری"))
    password1 = forms.CharField(label=("رمز عبور"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("تایید رمز عبور"),
        widget=forms.PasswordInput)  

    class Meta:
        model = User
        fields = ("username","email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(CustomForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user






class CustomLogin(forms.Form):
    username = forms.CharField(max_length=254, label=("نام کاربری"))
    password = forms.CharField(label=("رمز عبور"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': ("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(CustomLogin, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
        
