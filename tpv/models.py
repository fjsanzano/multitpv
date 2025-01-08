# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.db.models import Sum
# from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class TPV(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Punto de venta'
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Categoría'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductProduct(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Producto'

    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/uploads/%Y/%m/%d/')
    description = models.CharField(max_length=200)
    precio_costo = models.FloatField(default=0.0)
    precio_venta = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def get_stock_by_tpv(self, tpv):
        sale_id_list = [sale.pk for sale in Sale.objects.filter(tpv_id=tpv.id)]
        purchase_id_list = [purchase.pk for purchase in Purchase.objects.filter(tpv_id=tpv.id)]
        productos = []
        for producto in ProductProduct.objects.all():
            purchase_cant = PurchaseLine.objects.filter(purchase_id__in=purchase_id_list, product_id=producto.pk).aggregate(Sum('cant'))['cant__sum'] or 0
            sale_cant = SaleLine.objects.filter(sale_id__in=sale_id_list, product_id=producto.pk).aggregate(Sum('cant'))['cant__sum'] or 0
            productos.append({'name': producto.name,
                              'purchase_cant': purchase_cant,
                              'sale_cant': sale_cant,
                              'stock': purchase_cant - sale_cant
                              },
                             )
        return productos

    def get_stock_by_product(self, tpv):
        sale_id_list = [sale.pk for sale in Sale.objects.filter(tpv_id=tpv.id)]
        purchase_id_list = [purchase.pk for purchase in Purchase.objects.filter(tpv_id=tpv.id)]

        purchase_cant = PurchaseLine.objects.filter(purchase_id__in=purchase_id_list, product_id=self.pk).aggregate(Sum('cant'))['cant__sum'] or 0
        sale_cant = SaleLine.objects.filter(sale_id__in=sale_id_list, product_id=self.pk).aggregate(Sum('cant'))['cant__sum'] or 0

        return purchase_cant - sale_cant


class StockQuant(models.Model):
    class Meta:
        ordering = ('tpv_id', 'product_id')
        verbose_name = 'Existencia'

    tpv_id = models.ForeignKey(TPV, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductProduct, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.tpv_id.name+self.product_id.name


class Sale(models.Model):
    class Meta:
        ordering = ('tpv_id', 'sale_date')
        verbose_name = 'Venta'
    tpv_id = models.ForeignKey(TPV, on_delete=models.CASCADE)
    sale_date = models.DateTimeField("Fecha de venta", default=now)
    productos = models.ManyToManyField(ProductProduct, through='SaleLine')

    def __str__(self):
        return 'Venta '+str(self.id)+' '+self.tpv_id.name+' del '+self.sale_date.strftime('%Y-%m-%d %H:%M')


class SaleLine(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductProduct, on_delete=models.CASCADE)
    cant = models.IntegerField(default=1)
    precio_venta = models.FloatField(default=100)

    def clean(self):
        if self.product_id.get_stock_by_product(self.sale_id.tpv_id) <= 0:
            raise ValidationError("El producto %s no tiene existencia en ese punto de venta %s."% (self.product_id.name, self.sale_id.tpv_id.name))



class Purchase(models.Model):
    class Meta:
        ordering = ('tpv_id', 'purchase_date')
        verbose_name = 'Compra'

    tpv_id = models.ForeignKey(TPV, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField("Fecha de compra", default=now)
    productos = models.ManyToManyField(ProductProduct, through='PurchaseLine')

    def __str__(self):
        return 'Compra ' + str(self.id) + ' ' + self.tpv_id.name + ' del ' + self.purchase_date.strftime(
            '%Y-%m-%d %H:%M')


class PurchaseLine(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductProduct, on_delete=models.CASCADE)
    cant = models.IntegerField(default=1)
    precio_compra = models.FloatField(default=100.0)


