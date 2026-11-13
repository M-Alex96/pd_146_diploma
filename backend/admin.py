from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from backend.models import Shop, User, Category, Product, ProductInfo, Parameter, ProductParameter, Contact, Order, OrderItem

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(Parameter)
admin.site.register(ProductParameter)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(User)
class UserAdmin(UA):
    list_display = ('username', 'email', 'type', 'shop')
    list_filter = ('type', 'shop')
