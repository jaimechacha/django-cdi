import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from core.security.forms import ModuleTypeForm
from core.security.mixins import PermissionMixin
from core.security.models import *


class TypeListView(PermissionMixin, ListView):
    model = ModuleType
    template_name = 'moduletype/list.html'
    permission_required = 'view_moduletype'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('moduletype_create')
        context['title'] = 'Listado de Tipos de Módulos'
        return context


class TypeCreateView(PermissionMixin, CreateView):
    model = ModuleType
    template_name = 'moduletype/create.html'
    form_class = ModuleTypeForm
    success_url = reverse_lazy('moduletype_list')
    permission_required = 'add_moduletype'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if ModuleType.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'icon':
                if ModuleType.objects.filter(icon__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Tipo de Módulo'
        context['action'] = 'add'
        return context


class TypeUpdateView(PermissionMixin, UpdateView):
    model = ModuleType
    template_name = 'moduletype/create.html'
    form_class = ModuleTypeForm
    success_url = reverse_lazy('moduletype_list')
    permission_required = 'change_moduletype'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if ModuleType.objects.filter(name__iexact=obj).exclude(pk=id):
                    data['valid'] = False
            elif type == 'icon':
                if ModuleType.objects.filter(icon__iexact=obj).exclude(pk=id):
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
        context['title'] = 'Edición de un Tipo de Módulo'
        context['action'] = 'edit'
        return context


class TypeSortView(PermissionMixin, TemplateView):
    template_name = 'moduletype/sort.html'
    success_url = reverse_lazy('moduletype_list')
    permission_required = 'change_moduletype'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'sort':
                list_mod = []
                md_types = json.loads(request.POST['module_types'])
                for m in md_types:
                    instance = ModuleType.objects.get(id=m['id'])
                    instance.position = int(m['pos'])
                    list_mod.append(instance)
                ModuleType.objects.bulk_update(list_mod, ['position'])
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Ordenar tipos de módulos'
        context['action'] = 'sort'
        context['module_types'] = ModuleType.objects.filter(is_active=True).order_by('position')
        return context


class TypeDeleteView(PermissionMixin, DeleteView):
    model = ModuleType
    template_name = 'moduletype/delete.html'
    success_url = reverse_lazy('moduletype_list')
    permission_required = 'delete_moduletype'

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
