from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from bookings.models import Flight, Booking

def register_user(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User was created successfully.')
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration.')
    context = {
        'form':form
    }
    return render(request,'users/register.html',context)



def admin_login(request):
    page = 'Admin Login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('view_bookings')
        else:
            messages.error(request, 'Invalid credentials or not an admin user.')
    context = {
    'page':page
    }
    return render(request, 'users/login.html',context)


@login_required(login_url='admin_login')
@staff_member_required(login_url='admin_login')
def view_bookings(request):
    # Logic for admin dashboard view
    bookings = Booking.objects.all()
    return render(request, 'users/view-booking.html', {'bookings': bookings})


def login_user(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username Doesn't exist")
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully logged in.')
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username or Password is incorrect.')
            
    context = {
        'page':page
    }
    return render(request,'users/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')



@login_required(login_url='admin_login')
@staff_member_required(login_url='admin_login')
def add_flight(request):
    if request.method == 'POST':
        name = request.POST['name']
        destination = request.POST['destination']
        departure_date = request.POST['departure_date']
        departure_time = request.POST['departure_time']
        seat_count = request.POST['seat_count']
        
        flight = Flight.objects.create(
            name=name,
            destination=destination,
            departure_date=departure_date,
            departure_time=departure_time,
            seat_count=seat_count
        )
        return redirect('view_flights')  
    return render(request, 'users/add-flight.html')


@login_required(login_url='admin_login')
@staff_member_required(login_url='admin_login')
def view_flights(request):
    flights = Flight.objects.all()
    return render(request, 'users/view-flights.html', {'flights': flights})



@login_required(login_url='admin_login')
@staff_member_required(login_url='admin_login')
def update_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        flight.name = request.POST['name']
        flight.destination = request.POST['destination']
        flight.departure_date = request.POST['departure_date']
        flight.departure_time = request.POST['departure_time']
        flight.seat_count = request.POST['seat_count']
        flight.save()
        return redirect('view_flights')
    
    return render(request, 'users/update-flight.html', {'flight': flight})


@login_required(login_url='admin_login')
@staff_member_required(login_url='admin_login')
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        flight.delete()
        return redirect('view_flights')
    
    return render(request, 'users/delete-flight.html', {'flight': flight})

