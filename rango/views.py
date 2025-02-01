from django.shortcuts import render
from django.conf import settings
from rango.models import Category
from django.http import HttpResponse

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'rango/about.html', context_dict)