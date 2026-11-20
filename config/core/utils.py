from .models import Perfil

def es_admin(user):
    return hasattr(user, 'perfil') and user.perfil.tipo_usuario == 'admin'