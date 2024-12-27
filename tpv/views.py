from django.shortcuts import render
from datetime import date
# django library imports
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
# my apps imports
from .models import Sale
from django.shortcuts import render, redirect
from .forms import SaleForm, SaleLineForm

# Create your views here.

def home(request):
    # establishment_list = Establishment.objects.all()
    context = {}
    return render(request, 'home.html', context)


class SaleList(LoginRequiredMixin, ListView):
    model = Sale
    paginate_by = 100  # if pagination is desired
    template_name = "tpv/sale_list.html"

    def get_queryset(self):
        new_context = Sale.objects.all()
        return new_context


class SaleCreate(LoginRequiredMixin, CreateView):
    model = Sale
    fields = ['tpv_id', 'sale_date', 'productos']

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        # form.instance.reading_date = date.today
        return super().form_valid(form)


# class MeterReadingUpdate(UpdateView):
#     model = MeterReading
#     fields = ['contract_number']
#

class SaleDelete(LoginRequiredMixin, DeleteView):
    model = Sale
    success_url = reverse_lazy('sale-list')
    template_name = "tpv/sale_confirm_delete.html"


def add_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        saleline_form = SaleLineForm(request.POST)
        if sale_form.is_valid() and saleline_form.is_valid():
            factura = sale_form.save()
            detalle = saleline_form.save(commit=False)
            detalle.factura = factura
            detalle.save()
            return redirect('factura_lista')  # Cambia esto a la URL que desees
    else:
        sale_form = SaleForm()
        saleline_form = SaleLineForm()

    return render(request, 'tpv/add_sale_form.html', {
        'sale_form': sale_form,
        'saleline_form': saleline_form,
    })