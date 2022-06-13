from django.forms import Form, CharField, PasswordInput


class LoginForm(Form):
    username = CharField(required=True, max_length=50)
    password = CharField(required=True, widget=PasswordInput())
