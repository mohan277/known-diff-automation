from django import forms
from django.contrib.auth.hashers import check_password

from account.models import Users


class LoginModalForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=10, required=True)

    def clean_password(self):
        username = str(self.cleaned_data.get("username"))
        password = str(self.cleaned_data.get("password"))

        user = Users.objects.filter(username=username).first()
        if user:
            if not check_password(password, user.password):
                self.add_error("password", f"Invalid Credentials.")
        else:
            self.add_error("password", f"Invalid Credentials.")


class SignUpModalForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=10, required=True)

    def clean_username(self):
        username = str(self.cleaned_data.get("username"))
        if len(username.strip()) > 0 and Users.objects.filter(username=username.lower()).exists():
            self.add_error("username", f"Username already exists.")
        return username
