from django.urls import path

from musker.models import Profile


from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('profile_list/',views.profile_list,name='profile_list'),
]
