from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Creating meep mmodel
class Meep(models.Model):
    user = models.ForeignKey(User, related_name="meeps", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="meep_like", blank=True)

    # keep track or count of like
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user}" f"({self.created_at:%Y %m %d %H})" f"{self.body}...."


# Create A User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    # date_modified = models.DateTimeField(User, auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=200)
    facebook_link = models.CharField(null=True, blank=True, max_length=200)
    instagram_link = models.CharField(null=True, blank=True, max_length=200)
    linkedin_link = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.user.username


# Create profile when new User sign up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # have the user follow himself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


# post_save.connect(create_profile, sender=User)
