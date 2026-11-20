from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
        

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models
    def total(self):
        return sum(d.subtotal() for d in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
)

    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
class Perfil(models.Model):
    
    ROL_ADMIN = 'admin'
    ROL_CLIENTE = 'cliente'

    ROLES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_CLIENTE, 'Cliente'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    tipo_usuario = models.CharField(
        max_length=10,
        choices=ROLES,
        default=ROL_CLIENTE
    )

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"