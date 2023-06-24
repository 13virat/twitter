from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from musker.models import Meep, Profile

from .forms import MeepForm, ProfilePicForm, SignUpForms
from .models import Profile


def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, ("You meep has been posted"))
                return redirect("home")
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "home.html", {"meeps": meeps, "form": form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "home.html", {"meeps": meeps})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")


def unfollow(request, pk):
    if request.user.is_authenticated:
        # get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.remove(profile)
        # save our profile
        request.user.profile.save()
        # return message
        messages.success(
            request, (f"You have successfully unfolllowed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")
    
def follow(request, pk):
    if request.user.is_authenticated:
        # get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.add(profile)
        # save our profile
        request.user.profile.save()
        # return message
        messages.success(
            request, (f"You have successfully folllowed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")    


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
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

        return render(request, "profile.html", {"profile": profile, "meeps": meeps})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:

            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"profiles": profiles})
        else:
            messages.success(request, ("this is not your profile page"))
            return redirect("home")
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect("home")
        else:
            messages.success(request, ("there is an error plz try again"))
            return redirect("login")

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("you have been logged out"))
    return redirect("home")


def register_user(request):
    form = SignUpForms()
    if request.method == "POST":
        form = SignUpForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("you have been successfully registered"))
            return redirect("home")
    return render(request, "register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForms(
            request.POST or None, request.FILES or None, instance=current_user
        )
        profile_form = ProfilePicForm(
            request.POST or None, request.FILES or None, instance=profile_user
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("your info has been updated"))
            return redirect("home")

        return render(
            request,
            "update_user.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
    else:
        messages.success(request, ("you must be logged in to view that page..."))
        return redirect("home")


def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("you must be logged in to view that page..."))
        return redirect("home")


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(
            request,
            "show_meep.html",
            {"meep": meep},
        )

    else:
        messages.success(request, ("That meep does not exist..."))
        return redirect("home")
