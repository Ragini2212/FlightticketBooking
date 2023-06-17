from django.urls import path
from . import views



urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('flight/', views.flight_search, name='flight'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('my-booking/', views.my_bookings, name='my_bookings'),
]