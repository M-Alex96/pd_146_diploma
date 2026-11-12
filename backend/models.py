from django.contrib.auth.models import AbstractUser
from django.db import models

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

CONTACT_TYPE_CHOICES = (
    ('phone', 'Телефон'),
    ('address', 'Адрес'),
    ('email', 'Email'),
)

class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)

    def __str__(self):
        return self.username


class Shop(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100, unique=True)
    url = models.URLField(verbose_name="Ссылка")
    state = models.BooleanField(verbose_name="Статус получения заказов", default=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Список магазинов"
        ordering = ("-name",)

    def __str__(self):
        return self.name

class Category(models.Model):
    shops = models.ManyToManyField(Shop, verbose_name="Магазины", related_name='categories')
    name = models.CharField(verbose_name="Название", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Список категорий"
        ordering = ("-name",)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", related_name='products', on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=100)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"
        ordering = ("-name",)

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name="Магазин", related_name='product_infos', on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=100)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Стоимость")
    price_rrc = models.PositiveIntegerField(verbose_name="Рекомендуемая розничная стоимость")

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Информационный список о продуктах"
        constraints = [models.UniqueConstraint(fields=["product", "shop"], name="unique_product_shop")]

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"
        ordering = ("-name",)

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name="Информация о продукте", related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name="Параметр", related_name='product_parameters', on_delete=models.CASCADE)
    value = models.CharField(verbose_name="Значение", max_length=255)

    class Meta:
        verbose_name = "Параметр продукта"
        verbose_name_plural = "Список параметров продукта"
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter')
        ]

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name="Статус", choices=STATE_CHOICES, max_length=30)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Список заказов"
        ordering = ("-dt",)

    def __str__(self):
        return str(self.dt)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", related_name='order_items', on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, verbose_name="Информация о продукте", related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Заказанная позиция"
        verbose_name_plural = "Список заказанных позиций"
        constraints = [models.UniqueConstraint(fields=["order", "product_info"], name="unique_order_item")]

class Contact(models.Model):
    type = models.CharField(choices=CONTACT_TYPE_CHOICES, verbose_name="Тип контакта", max_length=100)
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name='contacts', on_delete=models.CASCADE)
    value = models.CharField(verbose_name="Значение", max_length=255)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Список контактов"
        constraints = [models.UniqueConstraint(fields=["user", "type", "value"], name="unique_user_contact")]
