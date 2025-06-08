from django import forms
from .models import Event, AppUser
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
    event_title = forms.CharField(max_length=200, help_text="Please enter event title ( [Artist Name] [Tour Name], [City] [Year] ): ")
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), help_text="Please enter the date of the event: ")
    venue = forms.CharField(max_length=75, help_text="Please enter name of the venue: ")
    city = forms.CharField(max_length=75, help_text="Please enter the city of the event: ")
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}), help_text="Please enter the start time for the event: ")
    artist = forms.CharField(max_length=50, help_text="Please enter the performing artist: ")
    capacity = forms.IntegerField(help_text="Please enter the venue capacity for this event: ")
    seats_booked = forms.IntegerField(help_text="Please enter no of seats booked (will default to 0): ", required=False)


    class Meta:

        model = Event
        exclude = ('date_added', 'slug')
    

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class AppUserForm(forms.ModelForm):

    profile_pic = forms.ImageField(required=False)
    bio = forms.CharField(help_text="(optional)", widget=forms.Textarea(), required=False)
    is_artist = forms.BooleanField(help_text="Are you an artist looking to post your events for fans?", widget=forms.CheckboxInput())
    stage_name = forms.CharField(help_text="(For artists)", required=False)

    class Meta:
        model = AppUser
        fields = ('profile_pic', 'bio', 'is_artist', 'stage_name')