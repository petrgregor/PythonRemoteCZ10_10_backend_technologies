from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.urls import reverse_lazy

# Create your views here.

# our signup form
class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

# our signup view
class SignUpView(generic.CreateView):  # CreateView pro vytváření nových objektů
    # připojíme formulář
    form_class = SignUpForm  # použijeme formulář definovaný výše
    success_url = reverse_lazy('login')  # kam nás to přesměruje, v případě úspěchu
    template_name = 'accounts/signup.html'  # použijeme tento tamplate
