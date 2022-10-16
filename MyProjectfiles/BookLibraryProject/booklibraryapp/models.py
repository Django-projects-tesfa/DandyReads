from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
#from sqlalchemy import null
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    #bio = models.TextField()
    verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    reported = models.IntegerField(default=0) 
    bagdeValue = models.IntegerField(default=0)

    #create profile whenever user is created.
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

class BooksLibrary(models.Model):
    userProfile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bookISBN13 = models.IntegerField(max_length=20)
    toReadList = models.BooleanField(default=False)
    completedReading = models.BooleanField(default=False)

    def __str__(self):
        # can be changed if needed
        return str(self.bookISBN13)
