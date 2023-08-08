from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Customer, OrderPlaced, cart as Cart
from django.views.generic import View
# from django.urls import reverse
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  return render(request, 'EcomApp/home.html', {'topwears':topwears,'bottomwears': bottomwears,
                                                     'mobiles':mobiles, 'laptop': laptops} )
 

class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_in_cart = False
  if request.user.is_authenticated:
    item_in_cart = Cart.objects.filter(Q(product=product.id) 
                                       & Q(user=request.user)).exists()
  return render(request, 'EcomApp/product_detail.html', {'product': product, 
                                                              'item_in_cart': item_in_cart})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'EcomApp/profile.html', {'form': form, 'active': 'btn-primary'})
  
  def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
            user = request.user
            name = form.cleaned_data.get('name')
            locality = form.cleaned_data.get('locality')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,f'Dear {name} your profile has been updated successfully')
      return render(request, 'EcomApp/profile.html', {'form': form, 'active': 'btn-primary'})

def add_to_cart(request):
    if request.user.is_authenticated:
      user = request.user
      product_id = request.GET.get('prod_id')
      product = Product.objects.get(id=product_id)
      Cart(user=user, product=product).save()
      return redirect('/cart') 
    else:
      return redirect('/login')
   

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discounted_price)
        amount += temp_amount
        total_amount = amount + shipping_amount
      return render(request, 'EcomApp/addtocart.html', {'cart': cart, 'total_amount': total_amount,
                                                         'amount': amount})
    else:
      return render(request, 'EcomApp/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity += 1
    c.save()
    amount = 0.0
    shipping_amount = 50.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discounted_price)
        amount += temp_amount
        total_amount = amount + shipping_amount

        data = {
          'quantity': c.quantity,
          'amount': amount,
          'total_amount': total_amount
        }
        return JsonResponse(data)
      
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()
    amount = 0.0
    shipping_amount = 50.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discounted_price)
        amount += temp_amount
        total_amount = amount + shipping_amount

        data = {
          'quantity': c.quantity,
          'amount': amount,
          'total_amount': total_amount
        }
        return JsonResponse(data)
      
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 50.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discounted_price)
        amount += temp_amount

        data = {
          'amount': amount,
          'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'EcomApp/buynow.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'EcomApp/address.html', {'add':add, 'active': 'btn-primary'})


def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
 return render(request, 'EcomApp/mobile.html', {'mobiles': mobiles})


def login(request):
 return render(request, 'EcomApp/login.html')

def customerregistration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username} account has been created! You are now able to log in')
            return redirect('customerregistration')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'EcomApp/customerregistration.html', {'form': form})



def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 50
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
   for p in cart_product:
     temp_amount = (p.quantity * p.product.discounted_price)
     amount += temp_amount
   total_amount = amount + shipping_amount
 return render(request, 'EcommerceApp/checkout.html', {'add': add, 'total_amount': total_amount,
                                                       'cart_items': cart_items})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'EcomApp/orders.html', {'order_placed': op})


def admin_view(request):
  customer_count = Customer.objects.all().count()
  product_count = Product.objects.all().count()
  order_count = OrderPlaced.objects.all().count()
  
  orders = OrderPlaced.objects.all()
  ordered_products = []
  ordered_persons = []

  for order in orders:
    ordered_product = Product.objects.filter(id=order.product.id)
    ordered_person = Customer.objects.filter(id=order.customer.id)
    ordered_products.append(ordered_product)
    ordered_persons.append(ordered_person)

  mydict = {
    'customer_count': customer_count,
    'product_count': product_count,
    'order_count': order_count,
    'data': zip(ordered_products,ordered_persons,orders),
  }
  return render(request, 'EcomApp/admin_dashboard.html',context= mydict)




    
    

