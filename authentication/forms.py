from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo', 'id':'user_email', 'class':'form-control'}),max_length=50,required=True,help_text='Se requiere un correo válido')
    username=forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario', 'id':'user_name', 'class':'form-control'}),max_length=50,required=True,help_text='Se requieren máximo 180 caracteres, digitos y  @/./+/-/_ únicamente.')
    password1=forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña', 'id':'user_password', 'class':'form-control'}),max_length=50,required=True,help_text='Tu contraseña debe contener mínimo 8 caracteres')
    password2=forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña', 'id':'confirm_password', 'class':'form-control'}),max_length=50,required=True,help_text='Ingresa la misma contraseña ingresada anteriormente')
    class Meta:
        model=User
        fields=['username','email','password1','password2']
class UserLoginForm(forms.Form):
    username=forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario', 'id':'user_name', 'class':'form-control'}),max_length=50)
    password=forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña', 'id':'user_password', 'class':'form-control'}),max_length=50,required=True)
    class Meta:
        model = User
        fields = ['username','password']
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña anterior',widget=forms.PasswordInput(attrs={'placeholder':'Ingresa tu contraseña anterior','class':'form-control'}),max_length=10,min_length=6,required=True)
    new_password1 = forms.CharField(label='Contraseña nueva',widget=forms.PasswordInput(attrs={'placeholder':'Ingresa tu nueva contraseña','class':'form-control'}),max_length=10,min_length=6,required=True)
    new_password2 = forms.CharField(label='Confirmar nueva contraseña',widget=forms.PasswordInput(attrs={'placeholder':'Confirmar nueva contraseña','class':'form-control'}),max_length=10,min_length=6,required=True)
    class Meta:
        model = PasswordChangeForm
        fields = ['old_password','new_password1','new_password2']

class RecoverPasswordForm(PasswordResetForm):
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo', 'id':'user_email', 'class':'form-control'}),max_length=50,required=True,help_text='Se requiere un correo electrónico válido')
    class Meta:
        models= PasswordResetForm
        fields = ['email']
class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nueva contraseña',widget=forms.PasswordInput(attrs={'placeholder':'Ingresar contraseña anterior'}),max_length=10,min_length=2,required=True)
    new_password2 = forms.CharField(label='Confirmar nueva contraseña',widget=forms.PasswordInput(attrs={'placeholder':'Ingresar contraseña anterior'}),max_length=10,min_length=2,required=True)
    class Meta:
        model=SetPasswordForm
        fields=['new_password1','new_password2']

class LockScreenForm(forms.Form):
    password=forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'placeholder': 'Ingresar tu contraseña', 'id':'user_password', 'class':'form-control'}),max_length=50,required=True)
    class Meta:
        model = User
        fields = ['password']