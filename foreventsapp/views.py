from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from django.urls import reverse
from foreventsapp.models import AppUser, Event, Booking
from foreventsapp.forms import AppUserForm, EventForm, UserForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout




def index(request):
    newest_added_events = Event.objects.order_by('-date_added')[:5]
    upcoming_events = Event.objects.filter(event_date__gte=datetime.now()).order_by('event_date')[:5] # I already ordered by recency in the Event model
    context = {'newest' : newest_added_events,
                'upcoming' : upcoming_events}

    return render(request, "index.html", context)


def aboutUs(request):
    return render(request, "aboutUs.html")
    

def events(request):
    events = Event.objects.all()
    context = {'events' : events}
    return render(request, "events.html", context)


def event(request, event_slug):
    try:
        event = get_object_or_404(Event, slug=event_slug)
        context = {'event' : event}
        return render(request, 'event.html', context)
    except Event.DoesNotExist:
        raise Http404("Specified event could not be found")
    
def add_event(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/foreventsapp/')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'add_event.html', context)


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = AppUserForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            print("Done")
            registered=True
            return redirect('/foreventsapp/')
        else:
            print("not done")
            print(user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form = AppUserForm()
    
    context = {}
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['registered'] = registered
    
    return render(request, 'register.html', context)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse('Your account has been disabled')
        else:
            return HttpResponse('Invalid login details')
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def profile(request):

    profile = request.user.profile
    users_events = Event.objects.filter(artist=profile, event_date__gte=datetime.now()).order_by('event_date')
    context = {'user' : profile, 'user_events' : users_events}
    print(profile.profile_pic.url)

    return render(request, 'profile.html', context)

def artist(request, name):

    artst = get_object_or_404(AppUser, stage_name=name)
    users_events = Event.objects.filter(artist=artst, event_date__gte=datetime.now()).order_by('event_date')

    if artst.stage_name != request.user.profile.stage_name:
        context = {'artist': artist, 'events': users_events}
        return render(request, 'artist.html', context)
    else:
        # Artist is the current user, send them to their profile page instead 
        return redirect(reverse('profile'))

def book_event(request, event_slug):
    booking = Booking.objects.get_or_create(event=Event.objects.get(slug= event_slug), user=request.user.profile)[1]
    if not booking:
        return HttpResponse("You have already booked this event")
    else:
        return redirect(reverse('profile'))


