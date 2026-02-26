from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, OnlineBooking

from .models import (
    OnlineBooking,
    OfflineBooking,
    Employee,
    Room,
    Salary,
    Authorregis
)

from .forms import (
    OnlineBookingForm,
    OfflineBookingForm,
    EmployeeForm,
    RoomForm,
    SalaryForm
)


# =========================
# BASIC PAGES
# =========================


def home(request):
    rooms = Room.objects.all().order_by('-id')[:6]  # Show latest 6 rooms
    return render(request, "Home.html", {"rooms": rooms})



# =========================
# AUTH SYSTEM
# =========================

@login_required
def dashboard(request):
    rooms = Room.objects.filter(status='available')[:6]
    return render(request, "dashboard.html", {"rooms": rooms})
from django.contrib.auth.decorators import login_required

@login_required
def user_home(request):
    rooms = Room.objects.all()
    user_bookings = OnlineBooking.objects.filter(user=request.user)

    return render(request, "user_home.html", {
        "rooms": rooms,
        "user_bookings": user_bookings
    })

def author_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")  # match your form fields
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone_number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("author_register")

        if Authorregis.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("author_register")

        user = Authorregis.objects.create_user(
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.phone_number = phone
        user.save()

        messages.success(request, "Registration successful!")
        return redirect("author_login")

    return render(request, "author_register.html")

def author_login(request):
    if request.method == "POST":
        email = request.POST.get("username")  # your form input is named "username"
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("user_home")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "author_login.html")

def author_forgot_password(request):
    # You can add actual reset logic later
    return render(request, "author_forgot_password.html")


def author_logout(request):
    logout(request)
    return redirect("home")


# =========================
# ONLINE BOOKING
# =========================

def online_booking(request):
    if request.method == "POST":
        form = OnlineBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful!")
            return redirect("online_booking")
    else:
        form = OnlineBookingForm()

    return render(request, "online_booking_page.html", {"form": form})


def online_booking_list(request):
    bookings = OnlineBooking.objects.all().order_by("-id")
    return render(request, "admin/Online_Booking.html", {"data": bookings})


def delete_online_booking(request, id):
    booking = get_object_or_404(OnlineBooking, pk=id)
    booking.delete()
    return redirect("online_booking_list")


# =========================
# OFFLINE BOOKING
# =========================

def add_customer(request):
    if request.method == "POST":
        form = OfflineBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully!")
            return redirect("add_customer")
    else:
        form = OfflineBookingForm()

    customers = OfflineBooking.objects.all().order_by("-id")
    return render(request, "admin/AddCustomer.html", {
        "form": form,
        "data": customers
    })


def delete_customer(request, id):
    customer = get_object_or_404(OfflineBooking, pk=id)
    customer.delete()
    return redirect("add_customer")


# =========================
# EMPLOYEE
# =========================

def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect("add_employee")
    else:
        form = EmployeeForm()

    employees = Employee.objects.all().order_by("-employee_id")
    return render(request, "admin/addemployee.html", {
        "form": form,
        "data": employees
    })


def delete_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()
    return redirect("add_employee")


# =========================
# ROOM
# =========================

# ROOM LIST PAGE
def room_list(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, "rooms.html", {"rooms": rooms})

def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added successfully!")
            return redirect("add_room")
    else:
        form = RoomForm()

    rooms = Room.objects.all().order_by("-id")
    return render(request, "admin/AddRoom.html", {
        "form": form,
        "data": rooms
    })


def delete_room(request, id):
    room = get_object_or_404(Room, pk=id)
    room.delete()
    return redirect("add_room")


# =========================
# SALARY
# =========================

def add_salary(request):
    if request.method == "POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary added successfully!")
            return redirect("add_salary")
    else:
        form = SalaryForm()

    salaries = Salary.objects.all().order_by("-id")
    return render(request, "admin/AddEmployeeSalary.html", {
        "form": form,
        "data": salaries
    })