# users/views.py

from django.views.generic import FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView  # ← добавлен LogoutView
from .forms import RegisterForm, ProfileForm
from .models import User
from django.contrib.auth import login, authenticate


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=email, password=password)  # используем email

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Не удалось войти после регистрации")
            return self.form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


