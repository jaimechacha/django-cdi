import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.school.forms import SchoolFeedingForm, SchoolFeeding
from core.security.mixins import  PermissionMixin


class SchoolFeedingListView(PermissionMixin, ListView):
    model = SchoolFeeding
    template_name = 'schoolfeeding/list.html'
    permission_required = 'view_schoolfeeding'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('schoolfeeding_create')
        context['title'] = 'Listado de Alimentación Escolar'
        return context


class SchoolFeedingCreateView(PermissionMixin, CreateView):
    model = SchoolFeeding
    template_name = 'schoolfeeding/create.html'
    form_class = SchoolFeedingForm
    success_url = reverse_lazy('schoolfeeding_list')
    permission_required = 'add_schoolfeeding'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Alimentación Escolar'
        context['action'] = 'add'
        return context


class SchoolFeedingUpdateView(PermissionMixin, UpdateView):
    model = SchoolFeeding
    template_name = 'schoolfeeding/create.html'
    form_class = SchoolFeedingForm
    success_url = reverse_lazy('schoolfeeding_list')
    permission_required = 'change_schoolfeeding'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Alimentación Escolar'
        context['action'] = 'edit'
        return context


class SchoolFeedingDeleteView(PermissionMixin, DeleteView):
    model = SchoolFeeding
    template_name = 'schoolfeeding/delete.html'
    success_url = reverse_lazy('schoolfeeding_list')
    permission_required = 'delete_schoolfeeding'

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

