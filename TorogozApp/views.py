from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password

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


## Desde aqui sirven las url

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Credenciales inválidas'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige de nuevo a la página de inicio de sesión

def home_view(request):
    return render(request, 'home.html')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('/home') 

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')

           
            common_passwords = ['123456', 'password', 'qwerty']  
            if password1 in common_passwords:
                form.add_error('password1', 'La contraseña es común. Por favor, elige una contraseña más segura.')

            
            if password1.lower() in username.lower():
                form.add_error('password1', 'La contraseña no puede contener el nombre de usuario.')

            if form.errors:
                return render(request, 'signup.html', {'form': form})
            
           
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
