# Create your models here.
from django.db import models


class TPV(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductProduct(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.FileField(upload_to='uploads/%Y/%m/%d/')
    description = models.CharField(max_length=200)
    precio_costo = models.IntegerField(default=0)
    precio_venta = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class StockQuant(models.Model):

    tpv_id = models.ForeignKey(TPV, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductProduct, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.tpv_id.name+self.product_id.name


class Sale(models.Model):
    tpv_id = models.ForeignKey(TPV, on_delete=models.CASCADE)
    sale_date = models.DateTimeField("Fecha de venta")


class SaleLine(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductProduct, on_delete=models.CASCADE)
    cant = models.IntegerField(default=1)
    precio_venta = models.IntegerField(default=100)
