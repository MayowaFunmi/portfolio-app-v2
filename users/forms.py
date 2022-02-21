from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import ContactMe, Project
from .models import Profile, City


# user signup form


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Your Password'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# form for user login:
class LoginForm(forms.Form):
    username = forms.CharField(help_text='Enter Your Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput, help_text='Enter Your Password', required=True) #widget=forms.PasswordInput


class ContactMeForm(forms.ModelForm):
    class Meta:
        model = ContactMe
        fields = "__all__"
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Address'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type Your Message Here...'}),
        }


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('slug', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Project Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Features'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Project Github Link'}),
            'demo_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Project Demo Link'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender', 'country', 'city', 'address', 'phone_number', 'profile_picture', 'interest', 'about_me']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Your Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number'}),
            'interest': forms.TextInput(attrs={'placeholder': 'What Topic(s) attract(s) You?'}),
            'about_me': forms.Textarea(attrs={'placeholder': 'Few Things About You...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

