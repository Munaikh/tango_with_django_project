from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'rango/about.html', context_dict)