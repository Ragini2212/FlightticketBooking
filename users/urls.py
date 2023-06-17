from django.urls import path
from . import views



urlpatterns = [
    path('',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('add-flight/', views.add_flight, name='add_flight'),
    path('view-flights/', views.view_flights, name='view_flights'),
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('flight/<int:flight_id>/update/', views.update_flight, name='update_flight'),
    path('flight/<int:flight_id>/delete/', views.delete_flight, name='delete_flight'),
]