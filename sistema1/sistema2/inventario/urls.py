
from django.urls import path
from . import views 
urlpatterns = [
    path('',views.principal1,name="principal"),
    path('principal2', views.principal2, name='principal2'),
    path('otro', views.principal3, name='principales'),
    path('programa1', views.programa1, name='prg1'),
    path('pag',views.programa2,name='prg2'),
    #path('prodreg',views.regproducto,name='prodadd'),
    path('inventario',views.menuPrincipal,name="menuprin"),
    path('productos',views.indexProd,name="indexprod"),
    path('productos/creaProd',views.creaProd,name="creaprod"), 
    path('productos/modificaProd',views.modificaProd,name="modprod"),

# ----------------------------------------------------------------------------
# ------------------PROYECTO BOLSA DE EMPLEOS MENU----------------------------
# ----------------------------------------------------------------------------
    
    path('principal',views.menuPriProyecto,name="menuPriPro"),
  
# --  PROYECTO BOLSA DE EMPLEO  -------     EMPLEOS    -----------------------

    path('Empleos',views.IndexEmp,name="indexEmpleos"),
    path('Empleos/crearempleos',views.CrearEmp,name="crearEmpleos"),   
    path('Empleos/modificacionempleos',views.ModificarEmp,name="modificarEmpleos"),   
    path('Empleos/formularioempleos',views.FormularioEmp,name="formularioEmpleos"),



    # URLs para la sección de Programadores
    path('programadores/', views.listar_programadores, name='listar_programadores'),
    path('programadores/nuevo/', views.crear_programador, name='crear_programador'),
    path('programadores/modificar/<int:pk>/', views.modificar_programador, name='modificar_programador'),
    path('programadores/eliminar/<int:pk>/', views.eliminar_programador, name='eliminar_programador'),
    path('blog/', views.listar_articulos, name='listar_articulos'),
    path('blog/<slug:slug>/', views.detalle_articulo, name='detalle_articulo'),
    path('empresas/', views.listar_empresas, name='listar_empresas'), # <-- ¡Este 'name' es el importante!
    path('empresas/<slug:slug_empresa>/', views.detalle_empresa, name='detalle_empresa'),
]
