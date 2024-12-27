from django import forms
from .models import Sale, SaleLine


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['id', 'tpv_id', 'sale_date']


class SaleLineForm(forms.ModelForm):
    class Meta:
        model = SaleLine
        fields = ['product_id', 'cant', 'precio_venta']