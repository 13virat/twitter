from django.contrib import messages
from django.shortcuts import redirect, render
from musker.models import Profile

from .models import Profile


def home(request):
    if request.user.is_authenticated:
    return render(request, "home.html", {})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        # Post form logic
        if request.method == "POST":
            # Get current User id
            current_user_profile = request.user.profile
            # get from data
            action = request.POST["follow"]
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # save profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")
