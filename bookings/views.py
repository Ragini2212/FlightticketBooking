from django.shortcuts import render

# Create your views here.


def home_view(request):
    return render(request,'bookings/home.html')


def flight_search(request):
    # Implement the flight search view
    return render(request, 'bookings/flight.html')



# bookings/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Flight, Booking

@login_required(login_url='login')
def home_view(request):
    if request.method == 'POST':
        print(request.POST)
        date = request.POST['departure_date']
        time = request.POST['departure_time']
        flights = Flight.objects.filter(departure_date=date, departure_time=time)
        return render(request, 'bookings/flight.html', {'flights': flights})
    return render(request, 'bookings/home.html')

@login_required(login_url='login')
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == 'POST':
        seat_count = int(request.POST['seat_count'])
        if seat_count <= flight.seat_count:
            booking = Booking(user=request.user, flight=flight, seat=seat_count)
            booking.save()
            flight.seat_count -= seat_count
            flight.save()
            return redirect('my_bookings')
        else:
            message = 'Sorry, there are not enough seats available.'
            return render(request, 'bookings/booking_failed.html', {'message': message})
    return render(request, 'bookings/book-flight.html', {'flight': flight})


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/user-booking.html', {'bookings': bookings})
