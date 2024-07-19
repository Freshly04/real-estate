from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProductRegisterForm
from .forms import UserRegisterForm, UserLoginForm, NewItemForm
from .models import Category, Product


# Create your views here.


def home(request):
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "core/home.html", context)


def signup(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:home")

    context = {"form": form}
    return render(request, "core/signup.html", context)


def login_view(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("core:home")

    context = {"form": form}
    return render(request, "core/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("core:login")


def category(request):
    all_categories = Category.objects.all()
    return {"all_categories": all_categories}


@login_required()
def add_item(request):
    form = NewItemForm()
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("core:home")

    context = {"form": form}
    return render(request, "core/new_item.html", context)


def item_detail(request, pk):
    product = Product.objects.get(pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)

    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "core/item_detail.html", context)


@login_required
def update_item(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    form = NewItemForm(instance=product)

    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
        return redirect("core:add-item")

    context = {
        "title": "Edit Product",
        "form": form,
    }
    return render(request, "core/new_item.html", context)


def delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)

    if request.method == "POST":
        product.delete()
    return redirect("core:home")

    context = {"product": product}
    return render(request, "core/delete.html", context)


def dashboard():
    products = Product.object.filter(created_by=request.user)

    context = {
        "products": products
    }
    return render(request, "core/dashboard.html", context)
