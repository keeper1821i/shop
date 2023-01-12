from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from app_users.models import Profile


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    patronymic = forms.CharField(max_length=20, required=False, help_text='Отчество')
    phone_number = forms.CharField(max_length=11, required=False, help_text='Номер телефона')
    email = forms.EmailField(max_length=70, required=False, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic', 'password1', 'password2', 'email')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileRedactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        last_name = kwargs['initial']['last_name']
        first_name = kwargs['initial']['first_name']
        email = kwargs['initial']['email']
        patronymic = kwargs['initial']['patronymic']
        photo = kwargs['initial']['photo']
        phone_number = kwargs['initial']['phone_number']

        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'name',
            'type': 'text',
            'data-validate': 'require',
            'value': f'{last_name} {first_name} {patronymic}'
        })

        self.fields['email'].widget = forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'mail',
            'name': 'mail',
            'type': 'text',
            'value': f'{email}',
            'data-validate': 'require'})

        self.fields['photo'].widget = forms.FileInput(attrs={
            'class': 'Profile-file form-input',
            'type': 'file',
            # 'data - validate': 'onlyImgAvatar',
            'value': photo

        })
        self.fields['phone_number'].widget = forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'phone',
            'name': 'phone',
            'type': 'text',
            'value': phone_number})

    name = forms.CharField(max_length=30)
    phone_number = forms.CharField(validators=[RegexValidator(
        "^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
        message='Пожалуйста, введите номер мобильного телефона в правильном формате! ')])

    email = forms.EmailField()
    password1 = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'id': 'password',
        'name': 'password',
        'type': 'password',
        'placeholder': 'Тут можно изменить пароль'}))
    password2 = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'id': 'passwordReply',
        'name': 'passwordReply',
        'type': 'password',
        'placeholder': 'Введите пароль повторно'}))
    photo = forms.ImageField(required=False)

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Пароли должны быть одинаковыми")
        else:
            return cleaned_data


    def clean_name(self):
        super().clean()
        name = self.cleaned_data.get('name')
        name = name.split(' ')
        if len(name) != 3:
            raise forms.ValidationError(message='Введите ФИО полностью через пробел')
        return name
