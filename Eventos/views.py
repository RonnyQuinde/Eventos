from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from Eventos.forms import RegistroUsuarioForm, EventoForm
from Eventos.models import Eventos


class ListaEventosView(LoginRequiredMixin, ListView):
    model = Eventos
    template_name = 'Eventos/lista_eventos.html'

    context_object_name = 'Eventos'

    def get_queryset(self):
        if self.request.user.rol == 'admin':
            return Eventos.objects.all()
        return Eventos.objects.filter(estado=True)

class DetalleEventoView(LoginRequiredMixin, DetailView):
    model = Eventos
    template_name = 'Eventos/detalle_evento.html'
    context_object_name = 'evento'

class InscribirEventoView(LoginRequiredMixin, DetailView):
    model = Eventos

    def get(self, request, *args, **kwargs):
        evento = self.get_object()
        if request.user not in evento.inscritos.all() and evento.inscritos.count() < evento.cupos:
            evento.inscritos.add(request.user)
            messages.success(request, f'Se ha inscrito exitosamente en el evento {evento.nombre}')
        else:
            messages.error(request, 'No se pudo realizar la inscripción. El evento puede estar lleno o ya está inscrito')
        return redirect('detalle_evento', pk=evento.pk)


class CrearEventoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Eventos
    form_class = EventoForm
    template_name = 'Eventos/eventos_form.html'
    success_url = reverse_lazy('lista_eventos')

    def test_func(self):
        return self.request.user.rol == 'admin'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El evento se ha creado correctamente')
        return response


class MisEventosView(LoginRequiredMixin, ListView):
    model = Eventos
    template_name = 'Eventos/lista_eventos.html'
    context_object_name = 'Eventos'

    def get_queryset(self):
        return self.request.user.Eventos_Inscritos.all()


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
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

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


