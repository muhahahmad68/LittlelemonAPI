from django.urls import path, include
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('menu-items', views.MenuItems.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()),
    path('cart/menu-items', views.CartItems.as_view()),
    path('orders', views.OrderItems.as_view()),
    path('orders/<int:pk>', views.SingleOrderItem.as_view()),
    path('groups/managers/users',views.ManagerView.as_view()),
    path('groups/managers/users/<int:id>', views.manager_delete),
    path('groups/delivery-crew/users', views.DeliveryView.as_view()),
    path('groups/delivery-crew/users/<int:id>', views.delivery_delete),
]
