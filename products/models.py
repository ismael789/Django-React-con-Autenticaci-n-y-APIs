from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Usuario de la tienda: inicia sesión con correo electrónico."""

    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    carrera = models.CharField('Carrera', max_length=120, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EmailUserManager()

    def __str__(self):
        return self.email

# Modelo de Categorias
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# Modelo de productos
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='get_products',
        verbose_name='Categoria'
    )
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    is_active = models.BooleanField(default=True)

    @classmethod
    def crear_con_categoria_default(cls, name, description, price):
        """Crea un producto y le asigna la categoria predeterminada."""
        categoria_default, _ = Category.objects.get_or_create(
            name='Sin categoria'
        )
        return cls.objects.create(
            name=name,
            description=description,
            price=price,
            category=categoria_default,
        )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name
