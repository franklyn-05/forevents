from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="User Profile", primary_key=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True, default='')
    is_artist = models.BooleanField()
    stage_name = models.CharField(max_length=100, blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        if self.stage_name:
            return self.stage_name
        else:
            return self.user.username
        

class Event(models.Model):
    tour_name = models.CharField(max_length=200)
    event_date = models.DateField("Event Date")
    venue = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    start_time = models.TimeField("Event Start Time")
    artist = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    seats_booked = models.IntegerField(default=0)
    slug = models.SlugField(primary_key=True, unique=True)
    date_added = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.artist} {self.tour_name}, {self.city} {self.event_date.year}")
        self.date_added = datetime.now()
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-event_date", "start_time"]
        unique_together = ["tour_name", "event_date", "city"]

    def __str__(self):
        return f"{self.artist} {self.tour_name}, {self.city} {self.event_date.year}"

    def is_full(self):
        return self.seats_booked >= self.capacity
    
    def seats_left(self):
        return self.capacity - self.seats_booked
    
    def nearly_sold_out(self):
        return (self.capacity - self.seats_booked) <= self.capacity / 10
        #True if less than 10% of seats are available to book

    def has_happened(self):
        return self.event_date >= datetime.now()



class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    time_booked = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.event.is_full():
            raise IndexError("Event is full")
        else:
            self.event.seats_booked += 1
            self.event.save()
            self.time_booked = datetime.now()
            super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.user.username} - {self.event}'
    
class Follow(models.Model):
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.followed_by.username} follows {self.user_followed.username}"
    
    def save(self, *args, **kwargs):
        self.user_followed.profile.followers += 1