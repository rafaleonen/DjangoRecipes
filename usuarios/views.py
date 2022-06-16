from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from receitas.models import Receita
from .forms import CadastroForm, CriaReceitaForm, LoginForm

def cadastro(request):
    
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            nome = form['nome'].value()
            email = form['email'].value()
            password = form['password'].value()
            if User.objects.filter(email=email).exists():
                print('Usuario já cadastrado')
                return redirect('cadastro')
            user = User.objects.create_user(username=nome, email=email, password=password)
            user.save()
            print('Usuario cadastrado com sucesso!')
            redirect('dashboard')
        else:
            contexto = { 'form': form }
            return render(request, 'usuarios/cadastro.html', contexto)
    
    else:
        form = CadastroForm()
        contexto = { 'form': form }
        return render(request, 'usuarios/cadastro.html', contexto)



def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form['email'].value()
            password = form['password'].value()
            if User.objects.filter(email=email).exists():
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()
                user = auth.authenticate(username=nome, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard')

    form = LoginForm()
    contexto = { 'form': form }

    return render(request, 'usuarios/login.html', contexto)

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=request.user.id)

        contexto = {
            'receitas': receitas
        }

        return render(request, 'usuarios/dashboard.html', contexto)
    return redirect('index')

def cria_receita(request):
    if request.method == 'POST':
        form = CriaReceitaForm(request.POST, request.FILES)
        
        if form.is_valid():
            nome_receita = form['nome_receita'].value()
            ingredientes = form['ingredientes'].value()
            modo_preparo = form['modo_preparo'].value()
            tempo_preparo = form['tempo_preparo'].value()
            rendimento = form['rendimento'].value()
            categoria = form['categoria'].value()
            foto_receita = request.FILES['foto_receita']
            user = get_object_or_404(User, pk=request.user.id)
            receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo,
                tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita, publicada=True)
            receita.save()
            return redirect('dashboard')
            
    form = CriaReceitaForm()
    contexto = {
        'form': form
    }
    return render(request, 'usuarios/cria_receita.html', contexto)

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    form = CriaReceitaForm()

    contexto = {
        'form': form,
        'receita': receita
    }

    return render(request,'usuarios/edita_receita.html', contexto)
