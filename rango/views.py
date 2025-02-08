from unicodedata import category
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
from django.http import HttpRequest


def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {}
    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    return render(request, "rango/index.html", context_dict)


def about(request):
    context_dict = {"MEDIA_URL": settings.MEDIA_URL}
    return render(request, "rango/about.html", context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict["category"] = category
        context_dict["pages"] = pages

    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "rango/category.html", context=context_dict)


def add_category(request: HttpRequest):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("rango:index"))
        else:
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request: HttpRequest, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse("rango:index"))

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(
                reverse(
                    "rango:show_category",
                    kwargs={"category_name_slug": category_name_slug},
                )
            )
        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context_dict)
