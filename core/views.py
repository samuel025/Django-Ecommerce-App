from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
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

class ItemDetailView(DetailView):
	model = Item
	template_name = "product-detail.html"
	

@login_required
def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
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
			)[0]
			order.items.remove(order_item)
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
				order.items.remove(order_item)
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
			# shipping_address_qs = Address.objects.filter(
			# 	user = self.request.user,
			# 	# default = True
			# 	)
			# if shipping_address_qs.exists():
			# 	context.update({'default_shipping_address': shipping_address_qs[0]})

		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("checkout")
		
		return render(self.request, "checkout-page.html", context)

	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
				# use_default_shipping = form.cleaned_data.get('use_default_shipping')
				# if use_default_shipping:
					
				# 	address_qs = Address.objects.filter(
				# 		user = self.request.user,
				# 		default = True
				# 		)
				# 	if address_qs.exists():
				# 		shipping_address = address_qs[0]
				# 		order.shipping_address = shipping_address
				# 		order.save()
				# 		return redirect("f_checkout")
				# 	else:
				# 		messages.warning(self.request, "No default address")
				# 		return redirect("checkout")
				# else:
				# 	print('User is entering new adrress')


					street_address = form.cleaned_data.get('street_address')
					apartment_address = form.cleaned_data.get('apartment_address')
					phone_number = form.cleaned_data.get('phone_number')
					# same_shipping_address = form.cleaned_data.get('same_shipping_address')
					# save_info = form.cleaned_data.get('save_info')

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
						

						# set_default_shipping = form.cleaned_data.get('set_default_shipping')
						# if set_default_shipping:
						# 	shipping_address.default = True
						# 	shipping_address.save()
						# 	return redirect('f_checkout')
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
