from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Cliente, Guia, Proveedor, AdminExtra, Inicio
from .forms import ClienteForm, GuiaForm, ProveedorForm, AdminExtraForm
from django.utils import timezone
import datetime


# views.py (fragmento / añadir estas importaciones al inicio del archivo)
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.contrib.auth.hashers import check_password, make_password
from django.core.signing import dumps, loads, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings



# ============================
# PÁGINAS ESTÁTICAS
# ============================


# Tiempo de validez en segundos (5 minutos)
TOKEN_MAX_AGE = 300
# Salt para el firmado (puedes dejar esto o cambiarlo)
TOKEN_SALT = "password-reset-salt-v1"


def recuperar(request):
    """
    Página donde el usuario escribe su correo. Si existe, se genera un token y se envía
    un link por correo. Si no existe, se muestra mensaje de error.
    """
    if request.method == "POST":
        correo = (request.POST.get("correo") or "").strip().lower()
        if not correo:
            messages.error(request, "Por favor ingresa un correo.")
            return render(request, "recuperar.html")

        # Buscar en las 4 tablas cuál contiene ese correo
        found_obj = None
        found_model_name = None
        for Modelo in (Cliente, Guia, Proveedor, AdminExtra):
            try:
                obj = Modelo.objects.get(correo=correo)
                found_obj = obj
                found_model_name = Modelo.__name__
                break
            except Modelo.DoesNotExist:
                continue

        if not found_obj:
            # correo no existe
            messages.error(request, "El correo no existe o esta erróneo.")
            return render(request, "recuperar.html")

        # Generar token firmado con info mínima: id, correo, modelo
        token_payload = {
            "id": found_obj.id,
            "correo": found_obj.correo,
            "model": found_model_name
        }
        token = dumps(token_payload, salt=TOKEN_SALT)

        # Construir URL absoluta hacia la vista recuperar_si
        url_path = reverse("recuperar_si")  # ejemplo: /recuperar/confirm/
        reset_url = request.build_absolute_uri(f"{url_path}?token={token}")

        # Preparar email
        subject = "Recuperación de contraseña - Intrepidos Aventura"
        message = (
            f"Has solicitado recuperar la contraseña para {correo}.\n\n"
            f"Abre este enlace en los próximos 5 minutos para cambiar tu contraseña:\n\n{reset_url}\n\n"
            f"Si no solicitaste esto, ignora este correo."
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
        recipient_list = [found_obj.correo]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, "El link se envio al correo dijitado.")
        except Exception as e:
            # Si falla el envío, informa (en desarrollo se usa console backend)
            messages.error(request, "Error enviando el correo. Revisa la configuración de email.")
            # opcional: registrar el error en logs
            print("Error sending password-reset email:", e)

        return render(request, "recuperar.html")

    # GET
    return render(request, "recuperar.html")




def recuperar_si(request):
    """
    Vista que recibe token (GET) y muestra formulario para cambiar contraseña,
    o procesa POST para actualizar la contraseña del usuario localizado por token.
    """
    if request.method == "GET":
        token = request.GET.get("token") or ""
        if not token:
            messages.error(request, "Enlace inválido o faltante.")
            return redirect("recuperar")

        # Validar token
        try:
            data = loads(token, max_age=TOKEN_MAX_AGE, salt=TOKEN_SALT)
        except SignatureExpired:
            messages.error(request, "El enlace ha expirado. Solicita uno nuevo.")
            return redirect("recuperar")
        except BadSignature:
            messages.error(request, "Enlace inválido.")
            return redirect("recuperar")

        # Token válido; renderizar formulario de cambio y pasar token oculto
        return render(request, "recuperarSI.html", {"token": token})

    # POST: procesar cambio de contraseña
    token = request.POST.get("token") or ""
    if not token:
        messages.error(request, "Solicitud inválida.")
        return redirect("recuperar")

    try:
        data = loads(token, max_age=TOKEN_MAX_AGE, salt=TOKEN_SALT)
    except SignatureExpired:
        messages.error(request, "El enlace ha expirado. Solicita uno nuevo.")
        return redirect("recuperar")
    except BadSignature:
        messages.error(request, "Enlace inválido.")
        return redirect("recuperar")

    correo = data.get("correo")
    model_name = data.get("model")
    obj_id = data.get("id")

    # Obtener clase modelo por nombre
    model_map = {
        "Cliente": Cliente,
        "Guia": Guia,
        "Proveedor": Proveedor,
        "AdminExtra": AdminExtra
    }
    Model = model_map.get(model_name)
    if not Model:
        messages.error(request, "Usuario no encontrado.")
        return redirect("recuperar")

    try:
        usuario_obj = Model.objects.get(id=obj_id, correo=correo)
    except Model.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect("recuperar")

    # Obtener nuevas contraseñas del formulario
    nueva = request.POST.get("nueva") or ""
    confirmar = request.POST.get("confirmar") or ""
    if not nueva or not confirmar:
        messages.error(request, "Debes rellenar ambos campos de contraseña.")
        return render(request, "recuperarSI.html", {"token": token})

    if nueva != confirmar:
        messages.error(request, "Las contraseñas no coinciden.")
        return render(request, "recuperarSI.html", {"token": token})

    # Guardar la nueva contraseña encriptada
    usuario_obj.password = make_password(nueva)
    usuario_obj.save()

    messages.success(request, "Contraseña cambiada con éxito. Ahora puedes iniciar sesión.")
    return redirect("login")



def viajes(request):
    usuario = request.session.get("usuario")
    return render(request, "viajes.html", {"usuario": usuario})

def viaje1(request):
    usuario = request.session.get("usuario")
    return render(request, "viaje1.html", {"usuario": usuario})

def viaje2(request):
    usuario = request.session.get("usuario")
    return render(request, "viaje2.html", {"usuario": usuario})

def viaje3(request):
    usuario = request.session.get("usuario")
    return render(request, "viaje3.html", {"usuario": usuario})

def destinos(request):
    usuario = request.session.get("usuario")
    return render(request, "destinos.html", {"usuario": usuario})

def destinos1(request):
    usuario = request.session.get("usuario")
    return render(request, "destinos1.html", {"usuario": usuario})

def destinos2(request):
    usuario = request.session.get("usuario")
    return render(request, "destinos2.html", {"usuario": usuario})

def destinos3(request):
    usuario = request.session.get("usuario")
    return render(request, "destinos3.html", {"usuario": usuario})

def destinos4(request):
    usuario = request.session.get("usuario")
    return render(request, "destinos4.html", {"usuario": usuario})

def reserva1(request):
    usuario = request.session.get("usuario")
    return render(request, "DesReserva1.html", {"usuario": usuario})

def reserva2(request):
    usuario = request.session.get("usuario")
    return render(request, "DesReserva2.html", {"usuario": usuario})

def reserva3(request):
    usuario = request.session.get("usuario")
    return render(request, "DesReserva3.html", {"usuario": usuario})

def reserva4(request):
    usuario = request.session.get("usuario")
    return render(request, "DesReserva4.html", {"usuario": usuario})

def guia(request):
    usuario = request.session.get("usuario")
    return render(request, "guia.html", {"usuario": usuario})

def guia1(request):
    usuario = request.session.get("usuario")
    return render(request, "guia1.html", {"usuario": usuario})

def guia2(request):
    usuario = request.session.get("usuario")
    return render(request, "guia2.html", {"usuario": usuario})

def guia3(request):
    usuario = request.session.get("usuario")
    return render(request, "guia3.html", {"usuario": usuario})

def guia4(request):
    usuario = request.session.get("usuario")
    return render(request, "guia4.html", {"usuario": usuario})

def guia5(request):
    usuario = request.session.get("usuario")
    return render(request, "guia5.html", {"usuario": usuario})

def guia6(request):
    usuario = request.session.get("usuario")
    return render(request, "guia6.html", {"usuario": usuario})

def via_reserva1(request):
    usuario = request.session.get("usuario")
    return render(request, "ViaReserva1.html", {"usuario": usuario})

def via_reserva2(request):
    usuario = request.session.get("usuario")
    return render(request, "ViaReserva2.html", {"usuario": usuario})

def via_reserva3(request):
    usuario = request.session.get("usuario")
    return render(request, "ViaReserva3.html", {"usuario": usuario})


# ============================
# REGISTRO
# ============================
def registrar(request):
    if request.method == "POST":
        rol = request.POST.get("rol")

        if rol == "usuario":  # Cliente
            form = ClienteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")
            return render(request, "registrar.html", {"form": form})

        elif rol == "guia":
            form = GuiaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")
            return render(request, "registrar.html", {"form": form})

        elif rol == "proveedor":
            form = ProveedorForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("login")
            return render(request, "registrar.html", {"form": form})

        elif rol == "admin":
            form = AdminExtraForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")
            return render(request, "registrar.html", {"form": form})

    return render(request, "registrar.html", {"form": None})


# ============================
# LOGIN
# ============================
def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("username")
        password = request.POST.get("password")

        usuario = None

        # Buscar en todos los modelos
        for modelo in (Cliente, Guia, Proveedor, AdminExtra):
            try:
                u = modelo.objects.get(correo=correo)
                if check_password(password, u.password):
                    usuario = {
                        "id": u.id,
                        "correo": u.correo,
                        "rol": modelo.__name__
                    }
                    break
            except modelo.DoesNotExist:
                continue

        if usuario:
            request.session["usuario"] = usuario  # Guardamos en sesión
            return redirect("inicio")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, "login.html")

    return render(request, "login.html")


# ============================
# LOGOUT
# ============================
def logout_view(request):
    request.session.flush()  # Cierra sesión
    return redirect("login")


# ============================
# INICIO
# ============================
def inicio(request):
    usuario = request.session.get("usuario")
    viajes = list(Inicio.objects.all()[:4])
    return render(request, "index.html", {
        "viajes": viajes,
        "usuario": usuario
    })


# ============================
# VALIDAR CORREO (AJAX)
# ============================
@require_GET
def validar_correo(request):
    correo = (request.GET.get('correo') or '').strip()
    exists = False
    if correo:
        exists = (
            Cliente.objects.filter(correo=correo).exists() or
            Guia.objects.filter(correo=correo).exists() or
            Proveedor.objects.filter(correo=correo).exists() or
            AdminExtra.objects.filter(correo=correo).exists()
        )
    return JsonResponse({'exists': exists})
