from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.db import connection
from django.http import HttpResponseServerError
from django.db import transaction
from .models import TablaBalanceGeneral,TablaCreditos,TablaRenovaciones
from django.contrib.auth.decorators import login_required
from datetime import datetime

#prueba
#prueba3
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

@login_required
def tablarutas(request):
    tablarutas1=TablaRutas.objects.all()
    total_cantidad = TablaRutas.objects.aggregate(total=Sum('cantidad'))['total']
    return render(request, 'tablarutas.html', {'tablarutas': tablarutas1, 'total_cantidad':total_cantidad})

@login_required
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
                return redirect('/home')  # Redirigir al usuario a su perfil
            else:
                msg = 'Error: Nombre de usuario o contraseña incorrectos.'
                return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def signout(request):
    logout(request)
    return redirect('/')


## Desde aqui sirven las url
@login_required
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige de nuevo a la página de inicio de sesión

@login_required
def home_view(request):
    registros_data, mes_actual, año_actual = homeTableM(request)
    registros_data2, mes_actual, año_actual = homeTCreReno(request)
    registros_data3 = sumaCreditoRenovacion(request)

    # Renderiza la plantilla 'home.html' con los datos obtenidos de homeTableM
    return render(request, 'home.html', {'registros': registros_data, 'registros2': registros_data2, 'registros3': registros_data3,'mes': mes_actual, 'año': año_actual})

@login_required
def tablabalancegeneral(request):
    registros_data, mes_actual, año_actual = homeTableM(request)
    registros_data2, mes_actual, año_actual = homeTCreReno(request)
    registros_data3 = sumaCreditoRenovacion(request)

    # Renderiza la plantilla 'home.html' con los datos obtenidos de homeTableM
    return render(request, 'tablabalance.html', {'registros': registros_data, 'registros2': registros_data2, 'registros3': registros_data3,'mes': mes_actual, 'año': año_actual})
@login_required
def tablacreditosyrenovaciones(request):
    registros_data, mes_actual, año_actual = homeTableM(request)
    registros_data2, mes_actual, año_actual = homeTCreReno(request)
    registros_data3 = sumaCreditoRenovacion(request)

    # Renderiza la plantilla 'home.html' con los datos obtenidos de homeTableM
    return render(request, 'tablacreditos_renovaciones.html', {'registros': registros_data, 'registros2': registros_data2, 'registros3': registros_data3,'mes': mes_actual, 'año': año_actual})


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
from django.shortcuts import render, redirect
from .models import SaldoTotal, TablaBalanceGeneral,TablaCreditos,TablaRenovaciones,TablaRutas

@login_required
def insertar_datos(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tipo = request.POST.get('tipo').upper()
        concepto = request.POST.get('concepto').upper()
        tipo_monto = request.POST.get('tipoMonto')
        monto = float(request.POST.get('montoHidden'))  

        saldo_total_obj = SaldoTotal.objects.first()
        saldo_total = saldo_total_obj.saldo_totalcol

        if tipo_monto in ['inversion', 'ingresos_a_caja', 'prestamo', 'cobros']:
            saldo_total += monto
        elif tipo_monto in ['creditos', 'renovaciones', 'salarios', 'prestamos_trabajadores', 'salidas']:
            saldo_total -= monto

        nuevo_registro = TablaBalanceGeneral(
            fecha=fecha,
            tipo=tipo,
            concepto=concepto,
            total=saldo_total,  
        )
        

        if tipo_monto in ['inversion', 'ingresos_a_caja', 'prestamo', 'cobros', 'creditos', 'renovaciones', 'salarios', 'prestamos_trabajadores', 'salidas']:
            setattr(nuevo_registro, tipo_monto, monto)

        try:
            with transaction.atomic():
                nuevo_registro.save()
                saldo_total_obj.saldo_totalcol = saldo_total
                saldo_total_obj.save()
                if tipo_monto == 'creditos':

                    if tipo in ['CREDITO 20 DIAS','CREDITOS 20 DIAS','CREDITO 20 DIA', 'CREDITO 30 DIAS','CREDITOS 30 DIAS','CREDITO 30 DIA', 'CREDITO 60 DIAS','CREDITOS 60 DIAS','CREDITO 60 DIA']:
                        #id_tabla_general1=obtenerultimoIDtablabalance()
                        #ultimo_id_creado = TablaBalanceGeneral.objects.latest('id_registro').id_registro
                        ultimo_registro_balance = TablaBalanceGeneral.objects.latest('id_registro')
                        nuevocredito = TablaCreditos(
                        fecha=fecha,
                        id_tabla_general=ultimo_registro_balance,
                        tipo_credito=tipo,
                        cantidad=monto
                        )
                        nuevocredito.save()
                elif tipo_monto == 'renovaciones':
                    if tipo in ['RENOVACION 20 DIAS', 'RENOVACION 30 DIAS', 'RENOVACION 60 DIAS']:
                        #id_tabla_general1=obtenerultimoIDtablabalance()
                        #ultimo_id_creado = TablaBalanceGeneral.objects.latest('id_registro').id_registro
                        ultimo_registro_balance = TablaBalanceGeneral.objects.latest('id_registro')
                        nuevorenovacion = TablaRenovaciones(
                        fecha=fecha,
                        id_tabla_general=ultimo_registro_balance,
                        tipo_renovacion=tipo,
                        cantidad=monto
                        )
                        nuevorenovacion.save()
                
                if 'RUTA' in concepto:
                    nuevo_registro_ruta = TablaRutas(
                        fecha=fecha,
                        tipo_ruta=concepto,
                        cantidad=monto
                    )
                    nuevo_registro_ruta.save()


            return redirect('home')  
        except Exception as e:
            
            return HttpResponseServerError("Error al guardar el registro: {}".format(str(e)))

    return render(request, 'home.html')
  
@login_required
def obtenerultimoIDtablabalance():
    with connection.cursor() as cursor:
        cursor.execute("select max(id_registro) from torogozapp_tablabalancegeneral limit 1;")           
    idmaximo = cursor.fetchone()
    if idmaximo[0] is not None:
        return idmaximo[0]
    else:
        return 0
@login_required    
def homeTableM(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MONTH(CURDATE()) AS mes, YEAR(CURDATE()) AS año")
        mes_año = cursor.fetchone()
        if mes_año:
            mes_actual = mes_año[0]
            año_actual = mes_año[1]

    # Obtener registros de TablaBalanceGeneral para el mes y año actual
    registros = TablaBalanceGeneral.objects.filter(fecha__month=mes_actual, fecha__year=año_actual).order_by('id_registro')
    registros_data = []

    for registro in registros:
        
        registros_data.append({
            'id_registro': registro.id_registro,
            'fecha': registro.fecha,
            'tipo': registro.tipo,
            'concepto': registro.concepto,
            'inversion': registro.inversion,
            'ingresos_a_caja': registro.ingresos_a_caja,
            'prestamo': registro.prestamo,
            'cobros': registro.cobros,
            'creditos': registro.creditos,
            'renovaciones': registro.renovaciones,
            'salarios': registro.salarios,
            'prestamos_trabajadores': registro.prestamos_trabajadores,
            'salidas': registro.salidas,
            'total': registro.total,
           
        })

    return registros_data, mes_actual, año_actual

@login_required
def mostrarXMesyAño(request):
    # Inicializar mes y año
    mes = None
    año = None

    # Obtener mes y año directamente de MySQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT MONTH(CURDATE()) AS mes, YEAR(CURDATE()) AS año")
        mes_año = cursor.fetchone()
        if mes_año:
            mes = mes_año[0]
            año = mes_año[1]

    return render(request, 'home.html', {'mes': mes, 'año': año})

@login_required
def homeTCreReno(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MONTH(CURDATE()) AS mes, YEAR(CURDATE()) AS año")
        mes_año = cursor.fetchone()
        if mes_año:
            mes_actual = mes_año[0]
            año_actual = mes_año[1]

    # Obtener registros de TablaCreditos para el mes y año actual
    registros_creditos = TablaCreditos.objects.filter(fecha__month=mes_actual, fecha__year=año_actual).order_by('fecha')#'-fecha'
    registros_renovaciones = TablaRenovaciones.objects.filter(fecha__month=mes_actual, fecha__year=año_actual).order_by('fecha')#'-fecha'

    registros_data2 = []

    for item in registros_creditos:
        registros_data2.append({
            'concepto': item.id_tabla_general.concepto,
            'fecha': item.fecha,
            'tipo': item.tipo_credito,
            'cantidad': item.cantidad,
        })

    for item in registros_renovaciones:
        registros_data2.append({
            'concepto': item.id_tabla_general.concepto,
            'fecha': item.fecha,
            'tipo': item.tipo_renovacion,
            'cantidad': item.cantidad,
        })



    return registros_data2, mes_actual, año_actual
@login_required
def sumaCreditoRenovacion(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MONTH(CURDATE()) AS mes, YEAR(CURDATE()) AS año")
        mes_año = cursor.fetchone()
        if mes_año:
            mes_actual = mes_año[0]
            año_actual = mes_año[1]

    # Obtener registros de TablaCreditos para el mes y año actual
    registros_creditos = TablaCreditos.objects.filter(fecha__month=mes_actual, fecha__year=año_actual)
    registros_renovaciones = TablaRenovaciones.objects.filter(fecha__month=mes_actual, fecha__year=año_actual)

    # Realiza las consultas para obtener las sumas de créditos por tipo y también las renovaciones
    creditos_20_dias = registros_creditos.filter(tipo_credito="credito 20 dias").aggregate(total=Sum('cantidad'))
    creditos_30_dias = registros_creditos.filter(tipo_credito="credito 30 dias").aggregate(total=Sum('cantidad'))
    creditos_60_dias = registros_creditos.filter(tipo_credito="credito 60 dias").aggregate(total=Sum('cantidad'))

    renovacion_20_dias = registros_renovaciones.filter(tipo_renovacion="renovacion 20 dias").aggregate(total=Sum('cantidad'))
    renovacion_30_dias = registros_renovaciones.filter(tipo_renovacion="renovacion 30 dias").aggregate(total=Sum('cantidad'))
    renovacion_60_dias = registros_renovaciones.filter(tipo_renovacion="renovacion 60 dias").aggregate(total=Sum('cantidad'))

    # Calcula el total de créditos
    total_creditos = (creditos_20_dias['total'] if creditos_20_dias['total'] else 0) + \
                     (creditos_30_dias['total'] if creditos_30_dias['total'] else 0) + \
                     (creditos_60_dias['total'] if creditos_60_dias['total'] else 0)

    # En este punto puedes hacer consultas adicionales para obtener las renovaciones si es necesario
    total_renovacion = (renovacion_20_dias['total'] if renovacion_20_dias['total'] else 0) + \
                     (renovacion_30_dias['total'] if renovacion_30_dias['total'] else 0) + \
                     (renovacion_60_dias['total'] if renovacion_60_dias['total'] else 0)
  

    # Retorna los resultados como un diccionario
    return {
        'creditos_20_dias': creditos_20_dias['total'] if creditos_20_dias['total'] else 0,
        'creditos_30_dias': creditos_30_dias['total'] if creditos_30_dias['total'] else 0,
        'creditos_60_dias': creditos_60_dias['total'] if creditos_60_dias['total'] else 0,
        'renovacion_20_dias': renovacion_20_dias['total'] if renovacion_20_dias['total'] else 0,
        'renovacion_30_dias': renovacion_30_dias['total'] if renovacion_30_dias['total'] else 0,
        'renovacion_60_dias': renovacion_60_dias['total'] if renovacion_60_dias['total'] else 0,
        'total_creditos': total_creditos,
        'total_renovacion': total_renovacion,
        
    }

#Views de la pagehistorial 
@login_required
def pageHistorial(request):
    return render(request, 'historial.html')
@login_required
def filtrarMestable(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MONTH(CURDATE()) AS mes, YEAR(CURDATE()) AS año")
        mes_año = cursor.fetchone()
        if mes_año:
            mes_actual = mes_año[0]
            año_actual = mes_año[1]

    # Obtener registros de TablaCreditos para el mes y año actual
    registros_creditos = TablaCreditos.objects.filter(fecha__month=mes_actual, fecha__year=año_actual).order_by('fecha')#'-fecha'
    registros_renovaciones = TablaRenovaciones.objects.filter(fecha__month=mes_actual, fecha__year=año_actual).order_by('fecha')#'-fecha'

    registros_data2 = []
    return 0

@login_required
def redirigir_a_admin(request):
    # Redirige al usuario a la página de administración
    return redirect('admin:index')
@login_required
def salir(request):
    logout(request)
    return redirect('/')

#---------------------------------------------------------------------------#
#historial
@login_required
def filtrar_por_mes(request):
    
    año_actual = datetime.now().year
    mes_actual = datetime.now().month

    
    with connection.cursor() as cursor:
        cursor.execute("SELECT YEAR(CURDATE()) AS año")
        año_actual_bd = cursor.fetchone()[0]

   
    if año_actual_bd:
        año_actual = año_actual_bd

    if request.method == 'GET':
        mes_seleccionado = request.GET.get('mes')
        año_seleccionado = request.GET.get('año', año_actual)

       
        if mes_seleccionado and mes_seleccionado != 'seleccion':
            try:
                mes_seleccionado = int(mes_seleccionado)
                registros_filtrados = TablaBalanceGeneral.objects.filter(fecha__month=mes_seleccionado, fecha__year=año_seleccionado)
                return render(request, 'historial.html', {'registros': registros_filtrados, 'año_actual': año_actual,'mes_actual': mes_actual})
            except ValueError:
                
                pass

    registros_todos = TablaBalanceGeneral.objects.filter(fecha__year=año_actual, fecha__month=datetime.now().month)
    return render(request, 'historial.html', {'registros': registros_todos, 'año_actual': año_actual,'mes_actual': mes_actual})

def mesActual(request):
    mes_actual = datetime.now().month
    return render(request, 'historial.html', {'mes_actual': mes_actual})
