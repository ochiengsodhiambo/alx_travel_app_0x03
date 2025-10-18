from django.urls import path
from . import views

urlpatterns = [
    path('', views.listings_list, name='listings-list'),

    # Chapa payment endpoints
    path('chapa/pay/', views.create_payment, name='chapa-pay'),
    path('chapa/verify/<str:booking_reference>/', views.verify_payment_status, name='chapa-verify'),
]
