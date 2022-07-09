from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
import random
import string
import json
from django.http import JsonResponse, response
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from .models import Item, OrderItem, Order, Address, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import redirect
# from .filters import ItemFilter
# Create your views here.
from .forms import CheckoutForm


def is_valid_form(values):
	valid = True
	for field in values:
		if field == '':
			valid = False
	return valid


class HomeView(ListView):
	def get(self, *args, **kwargs):
		Items = Item.objects.all()[:4]
		# myfilter = ItemFilter(self.request.GET, queryset = Items)
		# Items = myfilter.qs
		context = {'Item':Items}
		return render(self.request, "home.html", context)

class ShopView(ListView):
	def get(self, *args, **kwargs):
		Items = Item.objects.all()
		# myfilter = ItemFilter(self.request.GET, queryset = Items)
		# Items = myfilter.qs
		context = {'Item':Items}
		return render(self.request, "shop.html", context)

def ItemDetailView(request, slug):
	Items = Item.objects.get(slug=slug)
	context = {'object': Items}
	return render(request, 'product-detail.html', context)

@login_required
def add_to_cart(request, slug):
	if request.method == "POST":
		size = request.POST['size']
		color = request.POST['color']
		item = get_object_or_404(Item, slug=slug)
		if OrderItem.objects.filter(
			item=item,
			user=request.user,
			ordered=False,
		):
			dels = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False,
			)
			for q in dels:
				q.delete()
		order_item = OrderItem.objects.create(
		item=item,
		user=request.user,
		ordered=False,
		size = size,
		color = color
		)
		order_qs = Order.objects.filter(user=request.user, ordered=False)
		if order_qs.exists():
			order = order_qs[0]
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity += 1
				order_item.size = size
				order_item.color = color
				order_item.save()
				messages.info(request, "This item quantity was updated")
				return redirect('cart')
			else:
				messages.info(request, "This item was added to your cart")
				order.items.add(order_item)
				return redirect('cart')
		else:
			ordered_date = timezone.now()
			order = Order.objects.create(user=request.user, ordered_date=ordered_date)
			order.items.add(order_item)
			messages.info(request, "This item was added to your cart")
			return redirect('cart')
	else:
		try:
			item = get_object_or_404(Item, slug=slug)
			order_item = OrderItem.objects.get(
				item=item,
				user=request.user,
				ordered=False,
				)
			order_qs = Order.objects.filter(user=request.user, ordered=False)
			if order_qs.exists():
				order = order_qs[0]
				if order.items.filter(item__slug=item.slug).exists():
					order_item.quantity += 1
					order_item.save()
					messages.info(request, "This item quantity was updated")
					return redirect('cart')
				else:
					messages.info(request, "This item was added to your cart")
					order.items.add(order_item)
					return redirect('cart')
			else:
				ordered_date = timezone.now()
				order = Order.objects.create(user=request.user, ordered_date=ordered_date)
				order.items.add(order_item)
				messages.info(request, "This item was added to your cart")
				return redirect('cart')
		except ObjectDoesNotExist:
				return redirect('cart')

		

@login_required
def remove_from_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
			)[0].delete()
			# order.items.remove(order_item)
			messages.info(request, "This item was removed from your cart")
			return redirect('cart')
		else:
			messages.info(request, "This item is not in your cart")
			return redirect('product_page', slug=slug)	
	else:
		messages.warning(request, "You do not have an active order")
		return redirect('product_page', slug=slug)


@login_required
def remove_single_item_from_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order_item = OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
			)[0].delete()
			messages.info(request, "This item quantity was updated")
			return redirect('cart')
		else:
			messages.info(request, "This item is not in your cart")
			return redirect('product_page', slug=slug)	
	else:
		messages.info(request, "You do not have an active order")
		return redirect('product_page', slug=slug)

class Cart(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			
			order = Order.objects.get(user=self.request.user, ordered=False)
			context ={
				'object': order,
			}
			return render(self.request, 'cart.html', context)
		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("/")


class CheckoutView(View):
	def get(self, *args, **kwargs):	
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
	
			form = CheckoutForm()
			context={
			'form': form,
			'order': order
			
			}
	
		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("checkout")
		
		return render(self.request, "checkout-page.html", context)

	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
					street_address = form.cleaned_data.get('street_address')
					apartment_address = form.cleaned_data.get('apartment_address')
					phone_number = form.cleaned_data.get('phone_number')

					if is_valid_form([street_address, phone_number]):
						shipping_address = Address(
								user = self.request.user,
								street_address = street_address,
								apartment_address = apartment_address,
								phone_number = phone_number,
							) 
						shipping_address.save()
						order.shipping_address = shipping_address
						order.save()
						

						
						return redirect('f_checkout')

					else:
						messages.warning(self.request, "Please fill in the requred ")
						return redirect('f_checkout')		
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have active orders")
			return redirect('checkout')


class Contact(View):
	def get(self, *args, **kwargs):
		return render(self.request, 'contact.html', {})

def final_checkout(request):
	order = Order.objects.get(user=request.user, ordered=False)
	if order.shipping_address:
		context = {
					'order':order,
					}
		return render(request, 'final_checkout.html', context)
	else:
		messages.warning(request, "You have not added an address")
		return redirect("checkout")
		
def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentView(View):
	def get(self, *args, **kwargs):
		# transaction = Transaction(authorization_key = 'sk_test_4efc8832170a975a1e1eb669a89b512909d0049a')
		# response = transaction.verify(kwargs['id'])
		# data = JsonResponse(response, safe=False)
		paystack_secret_key = 'sk_test_4efc8832170a975a1e1eb669a89b512909d0049a'
		paystack = Paystack(secret_key=paystack_secret_key)
		response = Transaction.verify(reference=kwargs['id'])
		
				
	
		if response["status"] == True:
			try:
				order = Order.objects.get(user=self.request.user, ordered=False)
				payment = Payment()
				payment.paystack_id = kwargs['id']
				payment.user = self.request.user
				payment.amount = order.get_total()
				payment.save()

				order_items = order.items.all()
				order_items.update(ordered=True)
				for item in order_items:
					item.save()

				order.ordered = True
				order.payment = payment
				order.ref_code = create_ref_code()
				order.save()

				messages.success(self.request, "order was successful")
				return redirect("/")
			except ObjectDoesNotExist:
				messages.success(self.request, "Your order was successful")
				return redirect("/")
		else:
			messages.success(self.request, "Could not verify the transaction")
			return redirect("/")

def Payment_on_delivery(request):
	order = Order.objects.get(user=request.user, ordered=False)
	if order.shipping_address:
		context = {
					'order':order,
					}
		return render(request, 'pay_on_delivery.html', context)
		

def Pay_on_delivery(request):		
			try:
				order = Order.objects.get(user=request.user, ordered=False)

				order_items = order.items.all()
				order_items.update(ordered=True)
				for item in order_items:
					item.save()

				order.ordered = True
				order.ref_code = create_ref_code()
				order.save()

				messages.success(request, "order was successful")
				return redirect("/")
			except ObjectDoesNotExist:
				messages.success(request, "Your order was successful")
				return redirect("/")