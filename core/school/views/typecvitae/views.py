import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.school.forms import TypeCVitaeForm, TypeCVitae
from core.security.mixins import  PermissionMixin


class TypeCVitaeListView(PermissionMixin, ListView):
    model = TypeCVitae
    template_name = 'typecvitae/list.html'
    permission_required = 'view_typecvitae'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('typecvitae_create')
        context['title'] = 'Listado de Tipos de Curriculum Vitae'
        return context


class TypeCVitaeCreateView(PermissionMixin, CreateView):
    model = TypeCVitae
    template_name = 'typecvitae/create.html'
    form_class = TypeCVitaeForm
    success_url = reverse_lazy('typecvitae_list')
    permission_required = 'add_typecvitae'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if TypeCVitae.objects.filter(name__icontains=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Tipo de Curriculum Vitae'
        context['action'] = 'add'
        return context


class TypeCVitaeUpdateView(PermissionMixin, UpdateView):
    model = TypeCVitae
    template_name = 'typecvitae/create.html'
    form_class = TypeCVitaeForm
    success_url = reverse_lazy('typecvitae_list')
    permission_required = 'change_typecvitae'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'name':
                if TypeCVitae.objects.filter(name__icontains=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Tipo de Curriculum Vitae'
        context['action'] = 'edit'
        return context


class TypeCVitaeDeleteView(PermissionMixin, DeleteView):
    model = TypeCVitae
    template_name = 'typecvitae/delete.html'
    success_url = reverse_lazy('typecvitae_list')
    permission_required = 'delete_typecvitae'

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
