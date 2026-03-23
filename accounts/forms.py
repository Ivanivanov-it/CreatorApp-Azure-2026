import os

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username']



    def clean_username(self):
        username = self.cleaned_data['username']
        if UserModel.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']

class FullNameChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name']

class ProfilePictureChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['picture']

    def clean_picture(self):
        picture = self.cleaned_data['picture']

        if not picture:
            raise forms.ValidationError("No image selected.")

        if not hasattr(picture,'content_type'):
            return picture

        max_size = 2 * 1048 * 1048
        if picture.size > max_size:
            raise forms.ValidationError("Image size must not exceed 2MB.")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        extension = os.path.splitext(picture.name)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(f"Unsupported file type: Use: {', '.join(valid_extensions)}")

        valid_content_types = ['image/jpeg', 'image/png', 'image/webp']
        if picture.content_type not in valid_content_types:
            raise forms.ValidationError(f"Invalid image type.")

        from PIL import Image
        img = Image.open(picture)
        if img.width > 2000 or img.height > 2000:
            raise forms.ValidationError("Image dimensions must not exceed 2000x2000 pixels.")

        return picture