from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Profile

# Unregister groups
admin.site.unregister(Group)


# mix profile info user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Models
class UserAdmin(admin.ModelAdmin):
    model = User
    # Display username field on admin page
    fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial user
admin.site.unregister(User)

# Reregister user and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
