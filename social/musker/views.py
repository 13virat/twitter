from django.contrib import messages
from django.shortcuts import redirect, render
from musker.models import Profile,Meep

from .models import Profile


def home(request):
    if request.user.is_authenticated:
        meeps= Meep.objects.all().order_by("-created_at")
    return render(request, "home.html", {"meeps":meeps})


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
        meeps=Meep.objects.filter(user_id=pk).order_by("-created_at")
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

        return render(request, "profile.html", {"profile": profile,"meeps":meeps})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")
