from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Meep, Profile


# profile etra form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(
        label="Profile Bio",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Profile Bio"}
        ),
    )
    homepage_link = forms.CharField(
        label="Website Link",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Website Link"}
        ),
    )
    facebook_link = forms.CharField(
        label="Facebook Link",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Facebook Link"}
        ),
    )
    instagram_link = forms.CharField(
        label="Instagram Link",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Instagram Link"}
        ),
    )
    linkedin_link = forms.CharField(
        label="Linkedin Link",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Linkedin Link"}
        ),
    )

    class Meta:
        model = Profile
        fields = (
            "profile_image",
            "profile_bio",
            "homepage_link",
            "facebook_link",
            "instagram_link",
            "linkedin_link",
        )


class MeepForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter Your Musker Meep!",
                "class": "form-control",
            }
        ),
        label="",
    )

    class Meta:
        model = Meep
        exclude = (
            "user",
            "likes",
        )


class SignUpForms(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForms, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "forms-control"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "forms-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields[
            "password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields["password2"].widget.attrs["class"] = "forms-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
