from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from backend.models import Shop, User, Category, Product, ProductInfo, Parameter, ProductParameter, Contact, Order, OrderItem


@admin.register(User)
class UserAdmin(UA):
    list_display = ('email', 'first_name', 'last_name', 'type', 'shop', 'is_active')
    list_filter = ('type', 'shop', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = UA.fieldsets + (
        ('Дополнительно', {'fields': ('type', 'shop')}),
    )
    add_fieldsets = UA.add_fieldsets + (
        ('Дополнительно', {'fields': ('type', 'shop')}),
    )

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'state')
    list_filter = ('state',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('shops',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'model')

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'quantity', 'price', 'price_rrc')
    list_filter = ('shop',)
    search_fields = ('product__name',)

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('product_info', 'parameter', 'value')
    list_filter = ('parameter',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'phone', 'city')
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    list_filter = ('city',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_info', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'dt', 'total_sum_display', 'contact')
    list_filter = ('status', 'dt')
    search_fields = ('user__email', 'id')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('dt', 'total_sum_display')

    def total_sum_display(self, obj):
        return obj.total_sum
    total_sum_display.short_description = 'Сумма'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_info', 'quantity')
    list_filter = ('order__status',)