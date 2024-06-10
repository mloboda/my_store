import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from store.forms import AddQuantityForm, CheckoutForm, ProductFilterForm
from store.models import Product, Category, Order, OrderItem


def get_all_products(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')

        if sort_by == 'name_asc':
            products = products.order_by('name')
        elif sort_by == 'name_desc':
            products = products.order_by('-name')
        elif sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')

    return render(request, 'store/all_products.html', {'products': products, 'form': form})


def get_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_card.html', {'product': product})


def get_products_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')

        if sort_by == 'name_asc':
            products = products.order_by('name')
        elif sort_by == 'name_desc':
            products = products.order_by('-name')
        elif sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')

    template_name = f"store/{category_name.lower().replace(' ', '_')}.html"
    return render(request, template_name, {'products': products, 'form': form})


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=reverse_lazy('login'))
def view_cart(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'store/cart.html', context)


class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'store/cart.html'
    success_url = reverse_lazy('cart')


@login_required(login_url=reverse_lazy('login'))
def check_out(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                user_cart = Order.get_cart(request.user)
                form_data = form.cleaned_data
                user_cart.first_name = form_data['first_name']
                user_cart.last_name = form_data['last_name']
                user_cart.phone_number = form_data['phone_number']
                user_cart.city = form_data['city']
                user_cart.post_office = form_data['post_office']
                user_cart.save()
                user_cart.make_order()
                Order.objects.filter(user=request.user, status=Order.STATUS_CART).delete()
                return redirect('order_confirmation')
    else:
        form = CheckoutForm()
    return render(request, 'store/check_out.html', {'form': form})


def order_confirmation(request):
    return render(request, 'store/order_confirmation.html')


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status=Order.STATUS_CART)
    context = {'user': user, 'orders': orders}
    return render(request, 'store/profile.html', context)


def get_homepage(request):
    products = list(Product.objects.all())
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')

        if sort_by == 'name_asc':
            products = sorted(products, key=lambda x: x.name)
        elif sort_by == 'name_desc':
            products = sorted(products, key=lambda x: x.name, reverse=True)
        elif sort_by == 'price_asc':
            products = sorted(products, key=lambda x: x.price)
        elif sort_by == 'price_desc':
            products = sorted(products, key=lambda x: x.price, reverse=True)

    random_products = random.sample(products, min(len(products), 8))

    return render(request, 'store/home.html', {'products': random_products, 'form': form})


def about_us(request):
    return render(request, 'store/about_us.html')
