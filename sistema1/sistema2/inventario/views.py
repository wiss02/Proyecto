from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Programador
from .forms import ProgramadorForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def principal1(request):
    return HttpResponse("Pagina de principal de inventario")

def principal2(request):
    return HttpResponse("programa principal 2")

def principal3(request):
    return HttpResponse("programa principal 3 ejecutandose..........!!!")

def programa1(request):
    return render(request,"paginas/programa1.html")

def programa2(request):
    return render(request,"paginas/programa2.html")

#def regproducto(request):
#    return render(request,"productos/adiciona.html")

def menuPrincipal(request):
    return render(request,"paginas/principal.html")
# Create your views here.

# PRODUCTOS
def indexProd(request):
    return render(request,"productos/index.html")

def creaProd(request):
    return render(request,"productos/creaprod.html")

def modificaProd(request):
    return render(request,"productos/modificaprod.html")

# ----------------------------------------------------------------------------
# ------------------PROYECTO BOLSA DE EMPLEOS MENU----------------------------
# ----------------------------------------------------------------------------

def menuPriProyecto(request):
    return render(request,"paginas/baseMenuProyecto.html")

# --  PROYECTO BOLSA DE EMPLEO  -------     EMPLEOS    -----------------------

def IndexEmp(request):
    return render(request,"Empleos/Index.html")
 
def CrearEmp(request):
    return render(request,"Empleos/createEmp.html")

def ModificarEmp(request):
    return render(request,"Empleos/ModificaEmp.html")

def FormularioEmp(request):
    return render(request,"Empleos/fromEmp.html")
#-----------------------


def listar_programadores(request):
    programadores = Programador.objects.all()
    contexto = {
        'programadores': programadores
    }
    return render(request, 'Programadores/Index.html', contexto)

def crear_programador(request):
    if request.method == 'POST':
        form = ProgramadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_programadores') # Redirige a la lista después de crear
    else:
        form = ProgramadorForm()
    contexto = {
        'form': form,
        'titulo_pagina': 'Registrar Nuevo Programador'
    }
    return render(request, 'Programadores/crearProgramador.html', contexto)

def modificar_programador(request, pk): # pk es la llave primaria del programador
    programador_instancia = get_object_or_404(Programador, pk=pk)
    if request.method == 'POST':
        form = ProgramadorForm(request.POST, instance=programador_instancia)
        if form.is_valid():
            form.save()
            return redirect('listar_programadores')
    else:
        form = ProgramadorForm(instance=programador_instancia)
    contexto = {
        'form': form,
        'programador': programador_instancia, # Para mostrar info del programador si es necesario
        'titulo_pagina': 'Modificar Datos del Programador'
    }
    # Usaremos el mismo template de crear, pero pasaremos una instancia
    return render(request, 'Programadores/modificarProgramador.html', contexto)

def eliminar_programador(request, pk):
    programador_instancia = get_object_or_404(Programador, pk=pk)
    if request.method == 'POST': # Confirmación de eliminación usualmente es POST
        programador_instancia.delete()
        return redirect('listar_programadores')
    contexto = {
        'programador': programador_instancia
    }
    return render(request, 'Programadores/confirmarEliminarProgramador.html', contexto)


#aqui empieza la otra parte del codigo     del blog

# --- Importaciones de tus Modelos y Formularios ---
from .models import Programador, ArticuloBlog # <--- ASEGÚRATE DE IMPORTAR ArticuloBlog
from .forms import ProgramadorForm
# from .forms import ArticuloBlogForm # Si creas un formulario para el frontend del blog

# --- Tus vistas existentes (principal1, listar_programadores, etc.) ---
# ... (tus otras vistas van aquí) ...

# ++++++++++++++++++++++ INICIO VISTAS PARA EL BLOG ++++++++++++++++++++++

def listar_articulos(request):
    lista_de_articulos_publicados = ArticuloBlog.objects.filter(publicado=True).order_by('-fecha_publicacion')
    
    paginator = Paginator(lista_de_articulos_publicados, 5) # 5 artículos por página
    page_number = request.GET.get('page')
    try:
        articulos_pagina = paginator.page(page_number)
    except PageNotAnInteger:
        articulos_pagina = paginator.page(1)
    except EmptyPage:
        articulos_pagina = paginator.page(paginator.num_pages)
        
    contexto = {
        'articulos': articulos_pagina,
        'titulo_pagina': 'Nuestro Blog'
    }
    return render(request, 'Blog/listar_articulos.html', contexto)

def detalle_articulo(request, slug):
    articulo = get_object_or_404(ArticuloBlog, slug=slug, publicado=True)
    contexto = {
        'articulo': articulo,
        'titulo_pagina': articulo.titulo 
    }
    return render(request, 'Blog/detalle_articulo.html', contexto)


#empezando con seccion de las empresas -----------------------------
 
from .models import Programador, ArticuloBlog, Empresa, OfertaEmpleo # Asegúrate de importar Empresa y OfertaEmpleo
from .forms import ProgramadorForm
# from .forms import ... # Otros formularios que puedas tener

# --- Tus vistas existentes ---
# ... (principal1, listar_programadores, listar_articulos, etc.) ...

# ++++++++++++++++++++++ INICIO VISTAS PARA EMPRESAS ++++++++++++++++++++++

def listar_empresas(request):
    """
    Muestra una lista paginada de todas las empresas registradas.
    """
    lista_de_empresas = Empresa.objects.all().order_by('nombre') # Ordenar por nombre
    
    paginator = Paginator(lista_de_empresas, 9) # Muestra 9 empresas por página (puedes ajustar este número)
    page_number = request.GET.get('page')
    try:
        empresas_pagina = paginator.page(page_number)
    except PageNotAnInteger:
        empresas_pagina = paginator.page(1)
    except EmptyPage:
        empresas_pagina = paginator.page(paginator.num_pages)
        
    contexto = {
        'empresas': empresas_pagina,
        'titulo_pagina': 'Empresas Registradas'
    }
    return render(request, 'Empresas/listar_empresas.html', contexto)

def detalle_empresa(request, slug_empresa): # Cambiado pk a slug_empresa para usar el slug
    """
    Muestra el perfil detallado de una empresa y sus ofertas de empleo activas.
    """
    empresa = get_object_or_404(Empresa, slug=slug_empresa)
    # Obtenemos solo las ofertas de empleo publicadas de esta empresa
    ofertas_de_la_empresa = OfertaEmpleo.objects.filter(empresa=empresa, publicado=True).order_by('-fecha_publicacion')
    
    contexto = {
        'empresa': empresa,
        'ofertas_empleo': ofertas_de_la_empresa,
        'titulo_pagina': empresa.nombre
    }
    return render(request, 'Empresas/detalle_empresa.html', contexto)

# +++++++++++++++++++++++ FIN VISTAS PARA EMPRESAS ++++++++++++++++++++++++