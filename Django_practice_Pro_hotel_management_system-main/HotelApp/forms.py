from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from .models import Authorregis


class OnlineBookingForm(forms.ModelForm):
    class Meta:
        model = models.OnlineBooking
        fields = "__all__"

        


class OfflineBookingForm(forms.ModelForm):
    class Meta:
        model = models.OfflineBooking
        fields = "__all__"


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"


class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = "__all__"


class SalaryForm(forms.ModelForm):
    class Meta:
        model = models.Salary
        fields = "__all__"

class AuthorRegisterForm(UserCreationForm):
    class Meta:
        model = Authorregis
        fields = ['email', 'first_name', 'last_name', 'phone_number']