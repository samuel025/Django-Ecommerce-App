from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.forms import ModelForm
# Create your models here.

CATEGORY_CHOICES = (
	('Shirts', 'Shirts'),
	('Tops', 'Tops'),
	('Custom', 'Custom')
	)



class Color(models.Model):
	main_color = models.CharField(max_length=20)

	def __str__(self):
		return f"{self.main_color}"

class Color_Instance(models.Model):
	color_cloth = models.ManyToManyField(Color)



class Sizes(models.Model):
	main_size = models.CharField(max_length=20)

	def __str__(self):
		return f"{self.main_size}"

class Size_Instance(models.Model):
	size_cloth = models.ManyToManyField(Sizes)


class Item(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    another = models.TextField(blank=True, null=True)
    sizes_of_items = models.ForeignKey(Size_Instance, on_delete=models.CASCADE)
    color_of_items = models.ForeignKey(Color_Instance, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("product_page", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={'slug': self.slug})
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={'slug': self.slug})
    def __str__(self):
        return f"{self.title}"

class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	size = models.CharField(max_length=20)
	color = models.CharField(max_length=20)
	

	def __str__(self):
		return f"{self.quantity} of {self.item.title} size: {self.size}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_discount_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_price()
		return self.get_total_item_price()




class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ref_code = models.CharField(max_length=20)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,blank=True)
	payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True,blank=True)
	being_delivered = models.BooleanField(default=False)
	recieved = models.BooleanField(default=False)
	

class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=200)
	apartment_address = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=200)


class Payment(models.Model):
	paystack_id = models.CharField(max_length=30)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

# class OrderItemForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['size']s

