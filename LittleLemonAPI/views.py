from django.shortcuts import render
from rest_framework import generics, status
from .models import Menu, Category, Cart, Order, Delivery
from .serializers import MenuSerializer, CategorySerializer, Cartserializer, OrderSerializer,SingleOrderSerializer, DeliveryCrewSerializer, ManagerSerializer, CreateManagerSerializer, CreateDeliverySerializer, UpdateOrderSerializer, DeliverySerializer 
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAdminUser  # for permission granting
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .permissions import IsManagerOrReadOnly, IsManagerOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

def is_user_a_group_member(user, group_name): 
    try: 
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist: 
        return False
    
    return user.groups.filter(name=group_name).exists()
        

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItems(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsManagerOrReadOnly, )


class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsManagerOrReadOnly, )


class CartItems(generics.ListCreateAPIView, generics.DestroyAPIView):
    # queryset = Cart.objects.all()
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = Cartserializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

# Needs modification
class OrderItems(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    permission_classes = (DjangoModelPermissions, )

    def get(self, request, *args, **kwargs):
        query_user= self.request.user 
        if query_user.groups.filter(name='Delivery Crew').exists():
            print('Hello workd')
            order_user = Delivery.objects.filter(crew=query_user)
            queryset = DeliverySerializer(order_user, many=True)
            return Response(queryset.data)
        
        elif query_user.groups.filter(name='Manager').exists():
            all_orders = Order.objects.all()
            queryset = OrderSerializer(all_orders, many=True)
            return Response(queryset.data) 

        else: 
            print("it worked")
            order_user = Order.objects.filter(user=query_user)
            queryset = OrderSerializer(order_user, many=True)
            return Response(queryset.data)
      
        # return Response({
        #     'message': 'You need admin permission'
        # },status=status.HTTP_401_UNAUTHORIZED)

# Needs modification
class SingleOrderItem(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = SingleOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs['pk'])
    
    def put(self, request, pk):
        try:
            snippet = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # update
        serializer = UpdateOrderSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            del_order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # delete
        # manager_group = Group.objects.get(name="Manager")
        if self.request.user.groups.filter(name='Manager').exists():
            del_order.delete()
            return Response({
                'message': 'Deleted successfuly'
            },status=status.HTTP_204_NO_CONTENT)

        return Response({
                'message': 'You need admin permission'
            },status=status.HTTP_401_UNAUTHORIZED)
     
# Manager class
class ManagerView(generics.ListCreateAPIView):
    
    group = Group.objects.get(name="Manager")
    queryset = group.user_set.all()
    permission_classes = (IsManagerOnly, )

    def get_serializer_class(self):
        if self.request.method =='POST':
            # if self.request.user.groups.filter(name="Manager").exists():
            return CreateManagerSerializer
        return ManagerSerializer
            # return Response(status=status.HTTP_401_UNAUTHORIZED)

# Delivery crew class
class DeliveryView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle]
    group = Group.objects.get(name="Delivery Crew")
    queryset = group.user_set.all()
    permission_classes = (IsManagerOnly, )

    def get_serializer_class(self):
        if self.request.method =='POST':
            return CreateDeliverySerializer
        return DeliveryCrewSerializer
    
@api_view(['DELETE'])    
@csrf_exempt
@permission_classes((IsAdminUser, ))
def manager_delete(request, id):
    managers = Group.objects.get(name='Manager')
    user = get_object_or_404(User, id=id)
    managers.user_set.remove(user)
    return Response({f"Manager with id of {id} removed from manager group"})

@api_view(['DELETE'])    
@csrf_exempt
@permission_classes((IsAdminUser, ))
def delivery_delete(request, id):
    delivery_crew = Group.objects.get(name='Delivery Crew')
    user = get_object_or_404(User, id=id)
    delivery_crew.user_set.remove(user)
    return Response({f"User with id of {id} removed from delivery crew group"})


