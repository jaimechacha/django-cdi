import json

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.reports.forms import ReportForm
from core.school.forms import *
from core.security.mixins import PermissionMixin, ModuleMixin


class PeriodListView(PermissionMixin, ListView):
    model = Period
    template_name = 'period/list.html'
    permission_required = 'view_period'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Period.objects.filter():
                    data.append(i.toJSON())
            elif action == 'search_matters':
                data = []
                for i in PeriodDetail.objects.filter(period_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('period_create')
        context['title'] = 'Listado de Periodos'
        return context


class PeriodCreateView(PermissionMixin, CreateView):
    model = Period
    template_name = 'period/create.html'
    form_class = PeriodForm
    success_url = reverse_lazy('period_list')
    permission_required = 'add_period'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Period.objects.filter(name__icontains=obj):
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
        context['title'] = 'Nuevo registro de un Periodo'
        context['action'] = 'add'
        return context


class PeriodUpdateView(PermissionMixin, UpdateView):
    model = Period
    template_name = 'period/create.html'
    form_class = PeriodForm
    success_url = reverse_lazy('period_list')
    permission_required = 'change_period'

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
                if Period.objects.filter(name__icontains=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Periodo'
        context['action'] = 'edit'
        return context


class PeriodDeleteView(PermissionMixin, DeleteView):
    model = Period
    template_name = 'period/delete.html'
    success_url = reverse_lazy('period_list')
    permission_required = 'delete_period'

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


class PeriodAssignmentTeacherView(FormView):
    form_class = AssignmentTeacherPeriodForm
    template_name = 'period/assignment.html'
    success_url = reverse_lazy('period_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_matters_period':
                data = []
                for m in Matter.objects.filter():
                    item = m.toJSON()
                    status = PeriodDetail.objects.filter(period_id=self.kwargs['pk'],
                                                         matter_id=m.id,
                                                         contract_id=request.POST[
                                                             'contract']).exists()
                    item['status'] = 1 if status else 0
                    data.append(item)
            elif action == 'assignment_matters':
                with transaction.atomic():
                    instance = Period.objects.get(pk=self.kwargs['pk'])
                    
                    contract_id = request.POST['contract']
                    instance.perioddetail_set.filter(contract_id=contract_id).delete()
                    for m in json.loads(request.POST['matters']):
                        det = PeriodDetail()
                        det.period_id = instance.id
                        det.matter_id = m['id']
                        det.contract_id = contract_id
                        det.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = Period.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'Asignación de Curso Docente/Materias {}'.format(instance.name)
        context['list_url'] = self.success_url
        context['action'] = 'assignment_matters'
        return context


class PeriodTeacherConsultView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'period/consult_period_teacher.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_period':
                data = []
                
                period = request.POST['period']
                
                if len(period):
                    for i in PeriodDetail.objects.filter(period_id=period, contract__teacher__user=request.user):
                        data.append(i.toJSON())
            elif action == 'search_students':
                data = []
                for i in Matriculation.objects.filter(matriculationdetail__perioddetail_id=request.POST['id'],
                                                      matriculationdetail__perioddetail__contract__teacher__user=request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Materias por Periodos'
        return context
