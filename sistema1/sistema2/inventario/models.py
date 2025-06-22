from django.db import models

# Create your models here.
# inventario/models.py



from django.db import models
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User # Descomenta si decides usar autores
from django.utils.text import slugify

class Programador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, verbose_name="Especialidad")
    lenguajes = models.TextField(blank=True, help_text="Lenguajes que domina, separados por coma")
    experiencia_anios = models.IntegerField(default=0, verbose_name="Años de Experiencia")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Programador"
        verbose_name_plural = "Programadores"
        ordering = ['apellido', 'nombre']

class ArticuloBlog(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título del Artículo")
    slug = models.SlugField(max_length=250, unique_for_date='fecha_publicacion', blank=True, help_text="Versión amigable para URL, se autogenera del título si se deja vacío.")
    # autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articulos_blog', verbose_name="Autor")
    contenido = models.TextField(verbose_name="Contenido Completo del Artículo")
    resumen = models.TextField(max_length=500, blank=True, verbose_name="Resumen o Extracto", help_text="Breve resumen para la lista de artículos.")
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Publicación")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    # imagen_destacada = models.ImageField(upload_to='blog_imagenes_destacadas/', blank=True, null=True, verbose_name="Imagen Destacada")
    publicado = models.BooleanField(default=True, verbose_name="¿Publicado?")

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Artículo de Blog"
        verbose_name_plural = "Artículos del Blog"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('detalle_articulo', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
            original_slug = self.slug
            num = 1
            # Asegura unicidad del slug para la fecha de publicación
            while ArticuloBlog.objects.filter(
                slug=self.slug, 
                fecha_publicacion__year=self.fecha_publicacion.year,
                fecha_publicacion__month=self.fecha_publicacion.month,
                fecha_publicacion__day=self.fecha_publicacion.day
            ).exclude(id=self.id).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
        super().save(*args, **kwargs)

# aqui empieza la seccion de la empresa  

class Empresa(models.Model):
    nombre = models.CharField(max_length=200, unique=True, verbose_name="Nombre de la Empresa")
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="Versión amigable del nombre para la URL, se genera automáticamente.")
    logo = models.ImageField(upload_to='logos_empresas/', blank=True, null=True, verbose_name="Logo de la Empresa")
    descripcion = models.TextField(blank=True, verbose_name="Descripción de la Empresa")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio Web")
    email_contacto = models.EmailField(blank=True, null=True, verbose_name="Email de Contacto")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ciudad")
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sector Industrial")
    # usuario_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="empresas_gestionadas") # Opcional
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        # Asume que tendrás una URL llamada 'detalle_empresa' que toma un slug
        return reverse('detalle_empresa', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            # Lógica simple para asegurar unicidad del slug (puedes mejorarla si es necesario)
            original_slug = self.slug
            num = 1
            while Empresa.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
        super().save(*args, **kwargs)

# --- Modelo para Ofertas de Empleo ---
# Si ya tienes un modelo similar, adáptalo o asegúrate de que tenga una ForeignKey a Empresa.
# Si no lo tienes, este es un ejemplo básico:

class OfertaEmpleo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ofertas_empleo', verbose_name="Empresa")
    titulo_puesto = models.CharField(max_length=200, verbose_name="Título del Puesto")
    slug = models.SlugField(max_length=250, blank=True, help_text="URL amigable, se genera del título.") # Considera unique_for_date si es necesario
    descripcion_puesto = models.TextField(verbose_name="Descripción del Puesto")
    requisitos = models.TextField(blank=True, verbose_name="Requisitos")
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación del Puesto")
    tipo_contrato = models.CharField(max_length=50, blank=True, verbose_name="Tipo de Contrato", help_text="Ej: Tiempo Completo, Medio Tiempo, Freelance")
    salario_ofrecido = models.CharField(max_length=100, blank=True, null=True, verbose_name="Salario Ofrecido", help_text="Ej: Bs. 5000 - Bs. 7000, A convenir")
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Publicación")
    fecha_cierre_postulacion = models.DateField(blank=True, null=True, verbose_name="Fecha de Cierre de Postulación")
    email_para_postular = models.EmailField(blank=True, help_text="Email donde los candidatos deben enviar su CV.")
    enlace_externo_postulacion = models.URLField(blank=True, help_text="Enlace a un sistema de postulación externo si aplica.")
    publicado = models.BooleanField(default=True, verbose_name="¿Publicado?")
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Oferta de Empleo"
        verbose_name_plural = "Ofertas de Empleo"

    def __str__(self):
        return f"{self.titulo_puesto} en {self.empresa.nombre}"

    def get_absolute_url(self):
        # Esta URL es un ejemplo. Necesitarás definirla en tu urls.py para el detalle de la oferta.
        # Podría ser algo como '/empresas/<slug_empresa>/ofertas/<slug_oferta>/'
        # o '/ofertas/<pk_oferta>/'
        # Por ahora, lo dejaré comentado o simplificado, ya que depende de tu estructura de URLs para ofertas.
        # return reverse('detalle_oferta_empleo', args=[self.slug]) # Necesitarás una URL con este nombre
        pass # Implementa esto según tus URLs de detalle de oferta

    def save(self, *args, **kwargs):
        if not self.slug:
            # Crear un slug único para la oferta, podrías combinar el título y el id de la empresa o la fecha
            base_slug = slugify(self.titulo_puesto)
            self.slug = base_slug
            num = 1
            while OfertaEmpleo.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f'{base_slug}-{num}'
                num += 1
        super().save(*args, **kwargs)
