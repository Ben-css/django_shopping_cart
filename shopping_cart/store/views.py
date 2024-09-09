from http.client import ImproperConnectionState
from django.shortcuts import render
from .models import Product, Cart, CartItem
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())


def login(request):
    context = {}
     # 如果已經登入，直接跳轉到首頁
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')

    # 處理登入的 POST 請求
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        
        # 驗證成功，登入並跳轉
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            context['error'] = 'Invalid credentials. Please try again.'

    # 如果登入失敗，渲染登入頁面
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

@login_required
def index(request):
    cart = None
    created = False  # 預設為 False

    products = Product.objects.all()
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user,completed=False)
    else:
        # 未登入用戶使用 session 創建匿名購物車
        cart = request.session.get('cart', {})
        # 這裡可以執行對匿名購物車的操作，例如何時保存商品
        request.session['cart'] = cart
    
    context = {"products":products,"cart":cart}
    print(request.session.items(), request.COOKIES,)
    print("-------------------")
    print(cart,created)
    return render(request,'index.html',context)

@login_required
def cart(request):
    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user,completed=False)
        cartitems = cart.cartitems.all()
    context = {"cart":cart,"items":cartitems}
    return render(request, 'cart.html',context)

@login_required
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    # print(product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user,completed=False)
        # print(cart)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, products=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items
        print(cartitem, cartitem.quantity)

    return JsonResponse(num_of_item, safe=False)