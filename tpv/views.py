from django.shortcuts import render

# Create your views here.

def home(request):
    # establishment_list = Establishment.objects.all()
    context = {}
    return render(request, 'home.html', context)
