# inventario/forms.py
from django import forms
from .models import Programador

class ProgramadorForm(forms.ModelForm):
    class Meta:
        model = Programador
        fields = ['nombre', 'apellido', 'email', 'especialidad', 'lenguajes', 'experiencia_anios']
        # Puedes personalizar los widgets o labels si lo necesitas, por ejemplo:
        # labels = {
        # 'experiencia_anios': 'Años de Experiencia en la industria TI'
        # }
        # widgets = {
        # 'lenguajes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Python, JavaScript, Java'}),
        # }

    # Ejemplo de validación extra (opcional)
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre