from rest_framework import serializers
from .models import Menu, Category, Cart, Order, OrderItem, Delivery
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug', 'title']

class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        ordering_fields = ['price']
        filterset_fields = ['price', 'category']
        search_fields = ['title']

class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

# class AddCartItem(serializers.ModelSerializer):
    # class Meta:
        # model = Cart
        # fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Order
        fields = '__all__'
        ordering_fields = ['created_at']
        filterset_fields = ['created_at', 'status']
        search_fields = ['products']

class SingleOrderSerializer(serializers.ModelSerializer):
    products = MenuSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    
    def update(self, instance, validated_data):
        # instance.user = validated_data.get('user', instance.user)
        # instance.products = validated_data.get('products', instance.products)
        products = validated_data.pop('products', None)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if products:
            products_ = MenuSerializer(instance.user)
        return instance
        

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
        

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ] 

class CreateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def create(self):
        user = User.objects.get(username='username')
        group = Group.objects.get(name="Manager")
        group.user_set.add(user)

class DeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CreateDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def create(self):
        user = User.objects.get(username='username')
        group = Group.objects.get(name="Delivery crew")
        group.user_set.add(user)

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
 