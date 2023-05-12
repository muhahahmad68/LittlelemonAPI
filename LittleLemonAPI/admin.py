from django.contrib import admin
from .models import Category, Menu, Cart, Order, Delivery
# Register your models here.
admin.site.register(Menu)

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Delivery)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    prepopulated_fields = { 
        'slug' : ('title',),
    }