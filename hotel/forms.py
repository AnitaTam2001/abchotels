# hote1/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control',
        'placeholder': 'Enter your email address'
        })
    )

    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
        'placeholder': 'Enter your full name'
        })
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
        'placeholder': 'Enter your phone number'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # NO VALIDATION - ALL PASSWORDS ARE ALLOWED
        # Including "password", "12345678", etc.
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        # Split full name into first and last name
        full_name = self.cleaned_data['full_name']
        names = full_name.split(' ', 1) # Split into max 2 parts
        user.first_name = names[0]
        user.last_name = names[1] if len(names) > 1 else ''

        if commit:
            user.save()
            # Save phone number to UserProfile
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number:
                # Get or create UserProfile and update phone number
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.phone_number = phone_number
                profile.save()

        return user

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    contact_method = forms.ChoiceField(
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('both', 'Both')
        ],
        initial='email'
    )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'total_guests']
        widgets = {
            'guest_name': forms.TextInput(attrs={ 
                'class': 'form_input',
                'placeholder': 'Enter your full name'
            }),
            'guest_email': forms.EmailInput(attrs={ 
                'class': 'form_input',
                'placeholder': 'Enter your email address'
            }),
            'guest_phone': forms.TextInput(attrs={ 
                'class': 'form_input',
                'placeholder': 'Enter your phone number'
            }),
            'check_in': forms.DateInput(attrs={ 
                'type': 'date',
                'class': 'form_input'
            }),
            'check_out': forms.DateInput(attrs={ 
                'type': 'date',
                'class': 'form_input'
            }),
            'total_guests': forms.NumberInput(attrs={ 
                'class': 'form_input',
                'placeholder': 'Number of guests',
                'min': 1
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError("Check-out date must be after check-in date.")
            if (check_out - check_in).days < 1:
                raise forms.ValidationError("Minimum stay is 1 night.")
        return cleaned_data