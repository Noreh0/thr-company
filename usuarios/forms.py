import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


class CadastroForm(UserCreationForm):
    nome = forms.CharField(label='Nome completo', max_length=150)

    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'telefone')
        labels = {'email': 'E-mail', 'telefone': 'WhatsApp com DDD'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Repita a senha'
        self.fields['telefone'].widget.attrs.update({'inputmode': 'tel', 'autocomplete': 'tel-national', 'placeholder': '(41) 98888-7777'})
        self.fields['email'].widget.attrs.update({'autocomplete': 'email'})

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if len(email) > 150:
            raise forms.ValidationError('Use um e-mail com até 150 caracteres.')
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail. Entre ou use outro e-mail.')
        return email

    def clean_telefone(self):
        digitos = re.sub(r'\D', '', self.cleaned_data['telefone'])
        if digitos.startswith('55') and len(digitos) > 11:
            digitos = digitos[2:]
        if len(digitos) not in (10, 11):
            raise forms.ValidationError('Informe o DDD e o número, por exemplo (41) 98888-7777.')
        return digitos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.email  # o login é feito pelo e-mail
        usuario.first_name = self.cleaned_data['nome']
        if commit:
            usuario.save()
        return usuario


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail'
        self.fields['password'].label = 'Senha'

    def clean_username(self):
        usuario = self.cleaned_data['username'].strip()
        return usuario.lower() if '@' in usuario else usuario
