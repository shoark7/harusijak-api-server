from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Poet


class PoetLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Poet
        fields = ('identifier',)


class PoetCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Poet
        fields = ('identifier', 'nickname', 'image')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        poet = super().save(commit=False)
        poet.set_password(self.cleaned_data['password1'])
        poet.image = self.cleaned_data['image']
        if commit:
            poet.save()
        return poet


class poetChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Poet
        fields = ('identifier', 'password', 'nickname', 'image', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
