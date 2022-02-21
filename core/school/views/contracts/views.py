import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, UpdateView, DeleteView

from config import settings
from core.school.forms import ContractsForm, Contracts, User, Teacher
from core.security.mixins import PermissionMixin


class ContractsListView(PermissionMixin, FormView):
    model = Contracts
    form_class = ContractsForm
    template_name = 'contracts/list.html'
    permission_required = 'view_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for p in Contracts.objects.filter():
                    data.append(p.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('contracts_create')
        context['title'] = 'Listado de Profesores'
        return context


class ContractsCreateView(PermissionMixin, CreateView):
    model = Contracts
    template_name = 'contracts/create.html'
    form_class = ContractsForm
    success_url = reverse_lazy('contracts_list')
    permission_required = 'add_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = ContractsForm(excludefields=['state'])
        keys = list(Contracts.objects.filter(state=True).values_list('teacher', flat=True))
        keys = sorted(set(keys), key=keys.index)
        form.fields['teacher'].queryset = Teacher.objects.filter().exclude(id__in=keys)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                contract = Contracts()
               
                
                contract.job_id = int(request.POST['job'])
                contract.teacher_id = int(request.POST['teacher'])
                '''contract.shifts_id = int(request.POST['shifts'])'''
              
                contract.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Docente'
        context['action'] = 'add'
        return context


class ContractsUpdateView(PermissionMixin, UpdateView):
    model = Contracts
    template_name = 'contracts/create.html'
    form_class = ContractsForm
    success_url = reverse_lazy('contracts_list')
    permission_required = 'change_contracts'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = ContractsForm(instance=self.get_object(),
                             excludefields=['state'])
        form.fields['teacher'].widget.attrs.update({'disabled': True})
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                contract = self.object
                '''
                contract.start_date = request.POST['start_date']
                contract.end_date = request.POST['end_date']
                contract.shifts_id = int(request.POST['shifts'])
                contract.base_salary = float(request.POST['base_salary'])
                '''

                contract.job_id = int(request.POST['job'])
                contract.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Contrato'
        context['action'] = 'edit'
        return context


class ContractsDeleteView(PermissionMixin, DeleteView):
    model = Contracts
    template_name = 'contracts/delete.html'
    success_url = reverse_lazy('contracts_list')
    permission_required = 'delete_contracts'

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
