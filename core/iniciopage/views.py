import json

from django.http import HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.template.loader import render_to_string, get_template

from django.core.mail import send_mail
from django.conf import settings
from core.security.mixins import ModuleMixin
from core.iniciopage.models import Web
from core.iniciopage.forms import WebForm


# Create your views here.

# class IndexView(TemplateView):
#    template_name = 'inicio.html'

# class SuscripcionView(TemplateView):
#    template_name = 'suscripcion.html'

class ContactoView(TemplateView):
    template_name = 'contacto.html'

class NosotrosView(TemplateView):
    template_name = 'nosotros.html'


class WebUpdateView(ModuleMixin, UpdateView):
    template_name = 'create.html'
    form_class = WebForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        company = Web.objects.all()
        if company.exists():
            return company[0]
        return Web()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                comp = self.get_object()
                comp.name = request.POST['name']
                comp.ruc = request.POST['ruc']
                comp.mobile = request.POST['mobile']
                comp.email = request.POST['email']
                comp.address = request.POST['address']
                if 'image-clear' in request.POST:
                    comp.remove_image()
                if 'image' in request.FILES:
                    comp.image = request.FILES['image']
                comp.mission = request.POST['mission']
                comp.vision = request.POST['vision']
                comp.about_us = request.POST['about_us']
                comp.desc = request.POST['desc']
                comp.coordinates = request.POST['coordinates']
                comp.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Información del Sitio Web'
        context['action'] = 'edit'
        return context


def pagina(request):
    web = Web.objects.all()
    context = {"web": web}
    return render(request, "inicio.html", context)


class ActualizarWeb(ModuleMixin, UpdateView):
    model: Web
    form_class = WebForm
    template_name = 'ActualizarWeb.html'
    success_url = reverse_lazy("inicio")

    def get_queryset(self, *args, **kwargs):
        return Web.objects.filter(id=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Información del Sitio Web'
        context['action'] = 'edit'
        context['inicio'] = reverse_lazy('inicio')

        return context


def Suscripcion(request):
    if request.method == 'POST':
        ctx = {}
        action = request.POST.get('action')
        if action == 'estudiante':
            ctx['nomb_rpr'] = request.POST.get('nomb_rpr')
            ctx['apell_rpr'] = request.POST.get('apell_rpr')
            ctx['email_rpr'] = request.POST.get('email_rpr')
            ctx['ci_rpr'] = request.POST.get('ci_rpr')
            ctx['nomb_est'] = request.POST.get('nomb_est')
            ctx['apell_est'] = request.POST.get('apell_est')
            ctx['ci_est'] = request.POST.get('ci_est')
            ctx['direccion'] = request.POST.get('direccion')

        elif action == 'docente':
            ctx['nomb_doc'] = request.POST.get('nomb_doc')
            ctx['apell_doc'] = request.POST.get('apell_doc')
            ctx['email_doc'] = request.POST.get('email_doc')
            ctx['ci_doc'] = request.POST.get('ci_doc')
            ctx['cargo'] = request.POST.get('cargo')

        ctx['action'] = request.POST.get('action')
        ctx['tlf_conven'] = request.POST.get('tlf_conven') or 'Sin información'
        ctx['tlf_celular'] = request.POST.get('tlf_celular')
        ctx['fecha_naci'] = request.POST.get('fecha_naci')
        ctx['direccion'] = request.POST.get('direccion')
        ctx['opcion'] = request.POST.get('opcion')
        ctx['mensaje'] = request.POST.get('message') or 'Sin información'

        message = render_to_string('mail.html', ctx)
        send_mail('Solicitud de Suscripción',
                  message,
                  settings.EMAIL_HOST_USER,
                  ['jaimechacha256@gmail.com'],
                  fail_silently=False, html_message=message)
    return render(request, 'suscripcion.html')
