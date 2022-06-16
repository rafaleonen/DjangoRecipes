from django import forms

from usuarios.models import Usuario
from receitas.models import Receita
from .validation import *

# Form using forms.Form
class CadastroForm(forms.Form):
    nome = forms.CharField(label='Nome Completo',max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', strip=False, widget=forms.PasswordInput)

    def clean(self):
        nome = self.cleaned_data.get('nome')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        lista_de_erros = {}
        clean_name(nome, 'nome', lista_de_erros)
        field_not_strip(nome, 'nome', lista_de_erros)
        compare_passwords(password, password2, 'password2', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

# Form using forms.ModelForm
class LoginForm(forms.ModelForm):
    # add custom fields before class meta

    class Meta:
        model = Usuario
        # fields = ['email', 'password'] # '__all__' to use all fields
        exclude = ['nome'] # exclude only name field from fields
        labels = {'password': 'Senha' }
        widgets = {
            'password': forms.PasswordInput
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        lista_de_erros = {}
        field_not_strip(email, 'email', lista_de_erros)
        field_not_strip(password, 'password', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class CriaReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        exclude = ['pessoa', 'publicada', 'data_receita']
        labels = {
            'nome_receita': 'Nome da Receita',
            'modo_preparo': 'Modo de Preparo',
            'foto_receita': 'Foto'
        }
        wigets = {
            'foto_receita': forms.FileInput
        }

    def clean(self):
        return self.cleaned_data
