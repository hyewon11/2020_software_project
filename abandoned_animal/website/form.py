from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.db.transaction import commit
from .models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        widget = {'password':forms.PasswordInput}
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Error')
        return password2

    def save(self, commit=True):
        user=super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="비밀번호")

    class Meta:
        model = User
        fields = ('username','email','password')

