from django.shortcuts import render, redirect
from .models import Cliente, Producto, Pedido, DetallePedido, Perfil
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import es_admin
from django.db.models import Sum, F
from django.contrib import messages

@login_required
def lista_clientes(request):
    if request.user.perfil.tipo_usuario != 'admin':
        return redirect('/pedidos/')

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')

        try:
            Cliente.objects.create(nombre=nombre, telefono=telefono) 
            return redirect('/clientes/')
        except IntegrityError:
            return render(request, 'crear_cliente.html',{
                'error': 'Ya existe un cliente con ese telléfono'
            })

    return render(request, 'crear_cliente.html')

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.telefono = request.POST.get('telefono')

        try:
            cliente.save()
            return redirect('/clientes/')
        except IntegrityError:
            return render(request, 'editar_cliente.html', {
                'cliente': cliente,
                'error': 'Ya existe otro cliente con ese teléfono'
            })

    return render(request, 'editar_cliente.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('/clientes/')


@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})


@login_required
def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')

        try:
            Producto.objects.create(nombre=nombre, precio=precio, stock=stock)
            return redirect('/productos/')
        except IntegrityError:
            return render(request, 'crear_producto.html', {
                'error': 'El producto ya existe'
            })

    return render(request, 'crear_producto.html')


@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')

        try:
            producto.save()
            return redirect('/productos/')
        except IntegrityError:
            return render(request, 'editar_producto.html', {
                'producto': producto,
                'error': 'Ya existe un producto con ese nombre'
            })

    return render(request, 'editar_producto.html', {'producto': producto})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('/productos/')

@login_required
def lista_pedidos(request):
    if request.user.perfil.tipo_usuario == Perfil.ROL_ADMIN:
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)

    return render(request, 'pedidos.html', {'pedidos': pedidos})


@login_required
def crear_pedido(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')

        cliente = get_object_or_404(Cliente, id=cliente_id)  

        Pedido.objects.create(
            cliente=cliente,
            usuario=request.user
        )

        return redirect('/pedidos/')

    return render(request, 'crear_pedido.html', {'clientes': clientes})

@login_required
def agregar_productos(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    productos = Producto.objects.all()
    detalles = DetallePedido.objects.filter(pedido=pedido)

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))

        producto = Producto.objects.get(id=producto_id)

       
        if producto.stock < cantidad:
            messages.error(request, "Stock insuficiente")
            return redirect(f'/agregar-productos/{pedido.id}/')

        detalle, creado = DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio': producto.precio
            }
        )

        if not creado:
            detalle.cantidad += cantidad
            detalle.precio = producto.precio
            detalle.save()
        else:
            detalle.save()


        producto.stock -= cantidad
        producto.stock = max(producto.stock - cantidad, 0)
        producto.save()

        messages.success(request, "Producto agregado correctamente")
        return redirect(f'/agregar-productos/{pedido.id}/')

    return render(request, 'agregar_productos.html', {
        'pedido': pedido,
        'productos': productos,
        'detalles': detalles
    })


def login_view(request):

    if request.user.is_authenticated:
        if es_admin(request.user):
            return redirect('/clientes/')
        else:
            return redirect('/pedidos/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if es_admin(user):
                return redirect('/clientes/')
            else:
                return redirect('/pedidos/')
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def dashboard(request):

    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()

    ingresos = sum(p.total() for p in Pedido.objects.all())

    top_productos = list(
    DetallePedido.objects
    .values(nombre=F('producto__nombre'))
    .annotate(total=Sum('cantidad'))
    .order_by('-total')[:5]
)
    ultimos_pedidos = Pedido.objects.order_by('-id')[:5]

    context = {
        'clientes': total_clientes,
        'productos': total_productos,
        'pedidos': total_pedidos,
        'ingresos': ingresos,
        'top_productos': top_productos,
        'ultimos_pedidos': ultimos_pedidos,
    }

    return render(request, 'dashboard.html', context)