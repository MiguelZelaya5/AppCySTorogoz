from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html',{'form': form})
    else:
        form =UserCreationForm()
        return render(request, 'signup.html',{'form': form})

def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/profile')  # Si el usuario ya está autenticado, redirígelo a su perfil
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # Pasar la solicitud al formulario de autenticación
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Autenticar al usuario
                return redirect('/profile')  # Redirigir al usuario a su perfil
            else:
                msg = 'Error: Nombre de usuario o contraseña incorrectos.'
                return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')

def signout(request):
    logout(request)
    return redirect('/')
