from django.contrib import admin

# Register your models here.

from .models import TPV, ProductCategory, ProductProduct, StockQuant, Sale, SaleLine, Purchase, PurchaseLine


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')


admin.site.register(TPV)
admin.site.register(ProductProduct, ProductAdmin)
admin.site.register(ProductCategory)


class StockQuantAdmin(admin.ModelAdmin):
    list_display = ('tpv_id', 'product_id', 'cant')


admin.site.register(StockQuant, StockQuantAdmin)


class SaleLineInline(admin.TabularInline):
    model = SaleLine


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'tpv_id', 'sale_date')
    inlines = [
        SaleLineInline,
    ]


admin.site.register(Sale, SaleAdmin)


class PurchaseLineInline(admin.TabularInline):
    model = PurchaseLine


class Purchasedmin(admin.ModelAdmin):
    list_display = ('id', 'tpv_id', 'purchase_date')
    inlines = [
        PurchaseLineInline,
    ]


admin.site.register(Purchase, Purchasedmin)