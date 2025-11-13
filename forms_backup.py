# hotel/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import Booking, UserProfile, CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            # Create user profile with phone number
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
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
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out']
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
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'})
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