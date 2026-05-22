from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        help_text="Обязательное поле. Не более 150 символов. "
        "Только буквы, цифры и символы @/./+/-/_"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'unique': 'Уже существует'}
        
        self.fields['password1'].label = "Пароль"
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = "Ваш пароль должен содержать "
        "минимум 3 символа."
           
        self.fields['password2'].label = "Подтверждение пароля"
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].help_text = "Введите пароль ещё "
        "раз для проверки."
    

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        help_text="Обязательное поле. Не более 150 символов. "
        "Только буквы, цифры и символы @/./+/-/_"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label='Пароль')