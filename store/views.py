from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from store.forms import AddQuantityForm
from store.models import Product, Category, Order, OrderItem


def get_all_products(request):
    products = Product.objects.all()
    return render(request, 'store/all_products.html', {'products': products})


def get_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_card.html', {'product': product})


def get_products_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    template_name = f"store/{category_name.lower().replace(' ', '_')}.html"
    return render(request, template_name, {'products': products})


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
                return redirect('cart')

    return redirect('all_products')


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
def make_order(request):
    cart = Order.get_cart(request.user)
    cart.make_order()
    return redirect('all_products')
