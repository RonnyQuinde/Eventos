from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from Eventos.forms import RegistroUsuarioForm


class CustomLoginView(LoginView):
    template_name = 'registro/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos. Por favor, intente nuevamente.')
        return super().form_valid(form)

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Se ha cerrado la sesión exitosamente.')
        response = redirect('login')







class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registro/registro.html'
    success_url = reverse_lazy('lista_eventos')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Se ha registrado exitosamente")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
                return super().form_invalid(form)


