from django import forms

from contacts.models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model = Contact

        help_texts = {
            'email': 'Email so we can get back to you as soon as possible',
            'phone_number': "Optional phone number",
        }
        error_messages = {
            "first_name": {
                'max_length': "Your name is too long.",
                'required': "Please enter your name."
            },
            "last_name": {
                'max_length': "Your name is too long.",
                'required': "Please enter your name."
            },
            "phone_number": {
                'max_length': "Please enter a valid phone number.",
            },
            "email": {
                'required': "Please enter your email address.",
                'invalid': "Please enter a valid email address."
            },
            "content": {
                'required': "Please enter your message."
            }
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "First name (e.g. Ivan)",
            "last_name": "Last name (e.g. Ivanov)",
            "email": "Email address (e.g. Example@gmail.com)",
            "phone_number": "Phone number",
            "content" : "Description..."
        }
        for field,text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text