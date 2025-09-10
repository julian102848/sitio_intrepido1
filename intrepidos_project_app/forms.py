from django import forms
from django.contrib.auth.hashers import make_password
from .models import Cliente, Guia, Proveedor, AdminExtra

ADMIN_CODE = "INTREPIDOS-2024"


class ClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    nombre = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    apellido = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    telefono = forms.RegexField(regex=r'^\d+$', error_messages={'invalid': 'Solo números'})
    cedula = forms.RegexField(regex=r'^\d+$', error_messages={'invalid': 'Solo números'})

    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "correo", "telefono", "cedula", "password"]

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if (Cliente.objects.filter(correo=correo).exists() or 
            Guia.objects.filter(correo=correo).exists() or 
            Proveedor.objects.filter(correo=correo).exists() or 
            AdminExtra.objects.filter(correo=correo).exists()):
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirmar_password"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.password = make_password(self.cleaned_data["password"])
        if commit:
            cliente.save()
        return cliente


class GuiaForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    nombre = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    apellido = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    telefono = forms.RegexField(regex=r'^\d+$', error_messages={'invalid': 'Solo números'})
    cedula = forms.RegexField(regex=r'^\d+$', error_messages={'invalid': 'Solo números'})
    licencia = forms.RegexField(regex=r'^\d+$', error_messages={'invalid': 'Solo números'})
    poli = forms.ChoiceField(choices=[(True, "Sí"), (False, "No")], widget=forms.RadioSelect)

    class Meta:
        model = Guia
        fields = ["nombre", "apellido", "correo", "telefono", "cedula", "licencia", "poli", "password"]

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if (Cliente.objects.filter(correo=correo).exists() or 
            Guia.objects.filter(correo=correo).exists() or 
            Proveedor.objects.filter(correo=correo).exists() or 
            AdminExtra.objects.filter(correo=correo).exists()):
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirmar_password"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        guia = super().save(commit=False)
        guia.password = make_password(self.cleaned_data["password"])
        if commit:
            guia.save()
        return guia


class ProveedorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    nombre_proveedor = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    tipo_servicio = forms.RegexField(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', error_messages={'invalid': 'Solo letras'})
    certificado = forms.FileField(required=True)
    doc_representacion = forms.FileField(required=True)

    class Meta:
        model = Proveedor
        fields = ["nombre_proveedor", "tipo_servicio", "certificado", "doc_representacion", "correo", "password"]

    def clean_certificado(self):
        archivo = self.cleaned_data['certificado']
        if not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("El certificado debe ser un archivo PDF")
        return archivo

    def clean_doc_representacion(self):
        archivo = self.cleaned_data['doc_representacion']
        if not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("El documento debe ser un archivo PDF")
        return archivo

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if (Cliente.objects.filter(correo=correo).exists() or 
            Guia.objects.filter(correo=correo).exists() or 
            Proveedor.objects.filter(correo=correo).exists() or 
            AdminExtra.objects.filter(correo=correo).exists()):
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirmar_password"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        proveedor = super().save(commit=False)
        proveedor.password = make_password(self.cleaned_data["password"])
        if commit:
            proveedor.save()
        return proveedor


class AdminExtraForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AdminExtra
        fields = ["correo", "codigo_otorgado", "password"]

    def clean_codigo_otorgado(self):
        codigo = self.cleaned_data['codigo_otorgado']
        if codigo != ADMIN_CODE:
            raise forms.ValidationError("El código de administrador no es válido")
        return codigo

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if (Cliente.objects.filter(correo=correo).exists() or 
            Guia.objects.filter(correo=correo).exists() or 
            Proveedor.objects.filter(correo=correo).exists() or 
            AdminExtra.objects.filter(correo=correo).exists()):
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirmar_password"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.password = make_password(self.cleaned_data["password"])
        if commit:
            admin.save()
        return admin
