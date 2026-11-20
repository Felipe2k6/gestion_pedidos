from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.lista_clientes),
    path('crear-cliente/', views.crear_cliente),
    path('editar-cliente/<int:id>/', views.editar_cliente),
    path('eliminar-cliente/<int:id>/', views.eliminar_cliente),
    path('productos/', views.lista_productos),
    path('crear-producto/', views.crear_producto),
    path('editar-producto/<int:id>/', views.editar_producto),
    path('eliminar-producto/<int:id>/', views.eliminar_producto),
    path('pedidos/', views.lista_pedidos),
    path('crear-pedido/', views.crear_pedido),
    path('agregar-productos/<int:pedido_id>/', views.agregar_productos),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('dashboard/', views.dashboard),
]