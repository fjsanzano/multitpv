from django.contrib import admin

# Register your models here.

from .models import TPV, ProductCategory, ProductProduct, StockQuant, Sale, SaleLine


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')


admin.site.register(TPV)
admin.site.register(ProductProduct,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(StockQuant)


class SaleLineInline(admin.TabularInline):
    model = SaleLine


class SaleAdmin(admin.ModelAdmin):
    inlines = [
        SaleLineInline,
    ]


admin.site.register(Sale, SaleAdmin)