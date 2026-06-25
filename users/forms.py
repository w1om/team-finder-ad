import re

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_github_url(url):
    if url and "github.com" not in url.lower():
        raise forms.ValidationError("Ссылка должна вести именно на GitHub.")
    return url


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "email@example.com"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Придумайте пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar", "about", "phone", "github_url"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7XXXXXXXXXX"}
            ),
            "github_url": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "https://github.com/..."}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone

        cleaned_phone = phone.replace(" ", "").replace("-", "")

        if cleaned_phone.startswith("8"):
            cleaned_phone = "+7" + cleaned_phone[1:]

        if not re.match(r"^\+7\d{10}$", cleaned_phone):
            raise forms.ValidationError(
                "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
            )

        if User.objects.filter(phone=cleaned_phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже существует.")

        return cleaned_phone

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Текущий пароль введен неверно.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "Новые пароли не совпадают.")
        return cleaned_data