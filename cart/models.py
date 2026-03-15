from django.db import models
from django.contrib.auth.models import User
from main.models import Product

# Create your models here.

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']

    def __str__(self):
        return f'Корзина {self.user.username}'

    def get_total(self):
        """Получить общую сумму корзины"""
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = [['cart', 'product']]  # Чтобы товар не дублировался

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        """Стоимость позиции"""
        return self.product.price * self.quantity


class Order(models.Model):
    """Заказ пользователя"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        'Имя',
        max_length=100
    )
    phone = models.CharField(
        'Телефон',
        max_length=20
    )
    email = models.EmailField(
        'Email'
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )
    cart_data = models.JSONField(
        'Данные корзины',
        default=dict,
        help_text='Снимок товаров на момент заказа'
    )
    total = models.DecimalField(
        'Сумма заказа',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.name}'