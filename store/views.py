from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.core.paginator import Paginator
import json


from.models import*
from .forms import createUserForm

# Create your views here.

def registerPage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for' + user)
            return redirect('login')
            
    return render(
        request =request,
        template_name= 'store/register.html',
        context= {
            'form': form
        }
    )
    

def loginPage(request):
    if request.method =='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username OR password is incorrect')
            
    return render(
        request =request,
        template_name= 'store/login.html',
        context= {
            
        }
    )
    
def logoutUser(request):
    logout(request)
    return redirect('login')
    

def store(self, request):
    products = Product.objects.all()
    paginator = Paginator(products, 4)
    page_number = self.request.GET.get('page')
    print(page_number)
    products = paginator.get_page(page_number)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order ={'get_cart_items': 0, 'get_cart_total': 0 ,'shipping': False}
        cartItems = order['get_cart_items']
            
    return render(
        request= request,
        template_name= "store/store.html",
        context={
            'products': products,
            'cartItems':cartItems,
            
        }
    )

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order ={'get_cart_items': 0, 'get_cart_total': 0 ,'shipping': False}
        cartItems = order['get_cart_items']
    
    return render(
        request= request,
        template_name= "store/cart.html",
        context={
            'items': items,
            'order': order,
            'cartItems':cartItems,
        }
    )
    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items =[]
        order ={'get_cart_items': 0, 'get_cart_total': 0 ,'shipping': False}
        cartItems = order['get_cart_items']

        
    return render(
        request= request,
        template_name= "store/checkout.html",
        context={
            'items': items,
            'order': order,
            'cartItems':cartItems,
   
        }
    )

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action', action)
    print('productId', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    
    orderItem , created = OrderItem.objects.get_or_create(order = order, product= product)
    
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        

    return JsonResponse('Item was added', safe=False)
