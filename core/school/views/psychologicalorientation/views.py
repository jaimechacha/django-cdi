import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.school.forms import PsychologicalOrientationForm, PsychologicalOrientation
from core.security.mixins import  PermissionMixin


class PsychologicalOrientationListView(PermissionMixin, ListView):
    model = PsychologicalOrientation
    template_name = 'psychologicalorientation/list.html'
    permission_required = 'view_psychologicalorientation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in PsychologicalOrientation.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('psychologicalorientation_create')
        context['title'] = 'Listado de Orientaciones Psicológicas'
        return context


class PsychologicalOrientationCreateView(PermissionMixin, CreateView):
    model = PsychologicalOrientation
    template_name = 'psychologicalorientation/create.html'
    form_class = PsychologicalOrientationForm
    success_url = reverse_lazy('psychologicalorientation_list')
    permission_required = 'add_psychologicalorientation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                psyorient = PsychologicalOrientation()
                psyorient.date_joined = request.POST['date_joined']
                psyorient.desc = request.POST['desc']
                psyorient.matriculation_id = int(request.POST['matriculation'])
                psyorient.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Orientación Psicológica'
        context['action'] = 'add'
        return context


class PsychologicalOrientationUpdateView(PermissionMixin, UpdateView):
    model = PsychologicalOrientation
    template_name = 'psychologicalorientation/create.html'
    form_class = PsychologicalOrientationForm
    success_url = reverse_lazy('psychologicalorientation_list')
    permission_required = 'change_psychologicalorientation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                psyorient = self.object
                psyorient.date_joined = request.POST['date_joined']
                psyorient.desc = request.POST['desc']
                psyorient.matriculation_id = int(request.POST['matriculation'])
                psyorient.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Orientación Psicológica'
        context['action'] = 'edit'
        return context


class PsychologicalOrientationDeleteView(PermissionMixin, DeleteView):
    model = PsychologicalOrientation
    template_name = 'psychologicalorientation/delete.html'
    success_url = reverse_lazy('psychologicalorientation_list')
    permission_required = 'delete_psychologicalorientation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
