from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
	def get(self, request):
		totalitem = 0 #for badges i have created
		topwears = Product.objects.filter(category='TW')
		bottomwears = Product.objects.filter(category='BW')
		mobiles = Product.objects.filter(category='M')
		if request.user.is_authenticated:
			c = Cart.objects.filter( user=request.user)
			a = len(Cart.objects.filter(user=request.user))
			b=0
			for i in c:
				b+=i.quantity
			totalitem=b
		return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'totalitem':totalitem})


class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		item_already_in_cart=False
		if request.user.is_authenticated:
			c = Cart.objects.filter( user=request.user)
			a = len(Cart.objects.filter(user=request.user))
			b=0
			for i in c:
				b+=i.quantity
			totalitem=b
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

def mobile(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		c = Cart.objects.filter( user=request.user)
		a = len(Cart.objects.filter(user=request.user))
		b=0
		for i in c:
			b+=i.quantity
		totalitem=b
	if data==None :
			mobiles = Product.objects.filter(category='M')
	elif data == 'Redmi' or data == 'Samsung' or data=="iQOO" or data=="OPPO":
			mobiles = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
	elif data == 'above':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
	return render(request, 'app/mobile.html', {'mobiles':mobiles,'totalitem':totalitem})


def laptop(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		c = Cart.objects.filter( user=request.user)
		a = len(Cart.objects.filter(user=request.user))
		b=0
		for i in c:
			b+=i.quantity
		totalitem=b
	if data==None :
			laptops = Product.objects.filter(category='L')
	elif data == 'Lenovo' or data == 'MSI' or data=="HP" :
			laptops = Product.objects.filter(category='L').filter(brand=data)
	elif data == 'below':
			laptops = Product.objects.filter(category='L').filter(discounted_price__lt=25000)
	elif data == 'above':
			laptops = Product.objects.filter(category='L').filter(discounted_price__gt=25000)
	return render(request, 'app/laptop.html', {'laptops':laptops,'totalitem':totalitem})

def topwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		c = Cart.objects.filter( user=request.user)
		a = len(Cart.objects.filter(user=request.user))
		b=0
		for i in c:
			b+=i.quantity
		totalitem=b
	if data==None :
			topwears = Product.objects.filter(category='TW')
	elif data == 'Sangria' or data == 'SASSAFRAS' :
			topwears = Product.objects.filter(category='TW').filter(brand=data)
	elif data == 'below':
			topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=700)
	elif data == 'above':
			topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=700)
	return render(request, 'app/topwear.html', {'topwears':topwears,'totalitem':totalitem})

def bottomwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		c = Cart.objects.filter( user=request.user)
		a = len(Cart.objects.filter(user=request.user))
		b=0
		for i in c:
			b+=i.quantity
		totalitem=b
	if data==None :
			bottomwears = Product.objects.filter(category='BW')
	elif data == 'HM' or data == 'TokyoTalkies' or data=="SASSAFRAS" :
			bottomwears = Product.objects.filter(category='BW').filter(brand=data)
	elif data == 'below':
			bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=700)
	elif data == 'above':
			bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=700)
	return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears,'totalitem':totalitem})

class CustomerRegistrationView(View):
	def get(self, request):
		form = CustomerRegistrationForm()
		return render(request, 'app/customerregistration.html', {'form':form})
	
	def post(self, request):
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request, 'Congratulations!! Registered Successfully.')
			form.save()
			form = CustomerRegistrationForm()
		return render(request, 'app/customerregistration.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			c = Cart.objects.filter( user=request.user)
			a = len(Cart.objects.filter(user=request.user))
			b=0
			for i in c:
				b+=i.quantity
			totalitem=b
		form=CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form,'active':'btn-primary','totalitem':totalitem})
	
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			c = Cart.objects.filter( user=request.user)
			a = len(Cart.objects.filter(user=request.user))
			b=0
			for i in c:
				b+=i.quantity
			totalitem=b
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			location = form.cleaned_data['location']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			pincode = form.cleaned_data['pincode']
			reg = Customer(user=usr, name=name, location=location, city=city, state=state, pincode=pincode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
			form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary','totalitem':totalitem	})

@login_required
def add_to_cart(request):
	user = request.user
	product = request.GET.get('prod_id')
	product_title = Product.objects.get(id=product)	
	Cart(user=user, product=product_title).save()
	return redirect('/cart')

@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		c = Cart.objects.filter( user=request.user)
		a = len(Cart.objects.filter(user=request.user))
		b=0
		for i in c:
			b+=i.quantity
		totalitem=b
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 0.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
				totalamount = amount+shipping_amount
			return render(request, 'app/addtocart.html',{"carts":cart,'amount':amount, 'totalamount':totalamount,'totalitem':totalitem})
		else:
			return render(request, 'app/emptycart.html',{'totalitem':totalitem})
	else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})

	

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
	totalitem = 0
	c = Cart.objects.filter( user=request.user)
	a = len(Cart.objects.filter(user=request.user))
	b=0
	for i in c:
		b+=i.quantity
	totalitem=b
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add':add, 'active':'btn-primary','totalitem':totalitem })

def plus_cart(request):
	if request.method == 'GET':
		# a = len(Cart.objects.filter(user=request.user))
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 0.0
		totalitem=0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		# a = len(cart_product)
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)	
			amount += tempamount
			totalitem+=p.quantity
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount,
			"totalitem":totalitem
		}
		# print(data)
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 0.0
		totalitem=0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
			totalitem+=p.quantity
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount,
			"totalitem":totalitem
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 0.0
		totalitem=0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
			totalitem+=p.quantity
			
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount,
			"totalitem":totalitem
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount= 0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount=amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items,"totalamount":totalamount})

@login_required
def payment_done(request):
	custid = request.GET.get('custid')  #name filed helps gets the value of value in form
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		cid.delete()
	return redirect("orders")

@login_required
def orders(request):
	user = request.user
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'app/orders.html', {'order_placed':op,"user":user})
