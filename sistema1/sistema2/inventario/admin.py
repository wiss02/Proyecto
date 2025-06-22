# inventario/models.py

# inventario/admin.py

from django.contrib import admin
from .models import Programador, ArticuloBlog # IMPORTA TUS MODELOS DESDE .models

# Registro del modelo Programador
@admin.register(Programador)
class ProgramadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'experiencia_anios', 'fecha_actualizacion')
    search_fields = ('nombre', 'apellido', 'especialidad')
    list_filter = ('especialidad', 'fecha_actualizacion')

# Registro del modelo ArticuloBlog
@admin.register(ArticuloBlog)
class ArticuloBlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'fecha_publicacion', 'publicado')
    list_filter = ('publicado', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    # 'slug' se autogenera en el modelo, pero si quieres que el admin también ayude:
    prepopulated_fields = {'slug': ('titulo',)} 
    date_hierarchy = 'fecha_publicacion'
    # raw_id_fields = ('autor',) # Descomenta y ajusta si usas el campo autor como ForeignKey a User

#aqui empieza parte de la empresa /-*------------------

from .models import Programador, ArticuloBlog, Empresa, OfertaEmpleo # Asegúrate de importar Empresa y OfertaEmpleo


# --- NUEVO CÓDIGO PARA EMPRESAS Y OFERTAS DE EMPLEO ---
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'ciudad', 'sector', 'sitio_web')
    search_fields = ('nombre', 'descripcion', 'ciudad', 'sector')
    list_filter = ('ciudad', 'sector')
    prepopulated_fields = {'slug': ('nombre',)} # Ayuda a crear el slug automáticamente

@admin.register(OfertaEmpleo)
class OfertaEmpleoAdmin(admin.ModelAdmin):
    list_display = ('titulo_puesto', 'empresa', 'ubicacion', 'fecha_publicacion', 'publicado')
    list_filter = ('publicado', 'empresa', 'ubicacion', 'tipo_contrato', 'fecha_publicacion')
    search_fields = ('titulo_puesto', 'descripcion_puesto', 'empresa__nombre') # Puedes buscar por nombre de empresa
    date_hierarchy = 'fecha_publicacion'
    # raw_id_fields = ('empresa',) # Útil si tienes muchas empresas, muestra un input para el ID en lugar de un dropdown
    prepopulated_fields = {'slug': ('titulo_puesto',)}
    fieldsets = (
        (None, {
            'fields': ('empresa', 'titulo_puesto', 'slug', 'descripcion_puesto', 'requisitos', 'publicado')
        }),
        ('Detalles del Puesto', {
            'fields': ('ubicacion', 'tipo_contrato', 'salario_ofrecido')
        }),
        ('Fechas y Contacto', {
            'fields': ('fecha_publicacion', 'fecha_cierre_postulacion', 'email_para_postular', 'enlace_externo_postulacion')
        }),
    )