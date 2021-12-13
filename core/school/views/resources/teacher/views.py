import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.reports.forms import ReportForm
from core.school.forms import ResourcesForm, Resources, PeriodDetail
from core.security.mixins import PermissionMixin


class ResourcesTeacherListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'resources/teacher/list.html'
    permission_required = 'view_resources'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                period = request.POST['period']
                search = Resources.objects.filter(perioddetail__contract__teacher__user=request.user)
                if len(period):
                    search = search.filter(perioddetail__period__id=period)
                for d in search:
                    data.append(d.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('resources_teacher_create')
        context['title'] = 'Listado de Recursos'
        return context


class ResourcesTeacherCreateView(PermissionMixin, CreateView):
    model = Resources
    template_name = 'resources/teacher/create.html'
    form_class = ResourcesForm
    success_url = reverse_lazy('resources_teacher_list')
    permission_required = 'add_resources'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                date_range = request.POST['date_range'].split(' - ')
                resources = Resources()
                resources.start_date = date_range[0]
                resources.end_date = date_range[1]
                resources.perioddetail_id = int(request.POST['perioddetail'])
                resources.typeresource_id = int(request.POST['typeresource'])
                resources.web_address = request.POST['web_address']
                resources.desc = request.POST['desc']
                resources.save()
            elif action == 'search_matters':
                data = [{'id': '', 'text': '--------------'}]
                period = request.POST['period']
                if len(period):
                    for det in PeriodDetail.objects.filter(period_id=period, contract__teacher__user=request.user):
                        data.append({
                            'id': det.id,
                            'text': 'Nombre: {} / Nivel: {}'.format(det.matter.name, det.matter.get_level_display())
                        })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Recurso'
        context['action'] = 'add'
        return context


class ResourcesTeacherUpdateView(PermissionMixin, UpdateView):
    model = Resources
    template_name = 'resources/teacher/create.html'
    form_class = ResourcesForm
    success_url = reverse_lazy('resources_teacher_list')
    permission_required = 'change_resources'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ResourcesForm(instance=instance, initial={
            'period': instance.perioddetail.period.id,
            'date_range': '{} - {}'.format(instance.start_date, instance.end_date)
        })
        form.fields['perioddetail'].queryset = PeriodDetail.objects.filter(period_id=instance.perioddetail.period.id,
                                                                           contract__teacher__user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                date_range = request.POST['date_range'].split(' - ')
                resources = self.object
                resources.start_date = date_range[0]
                resources.end_date = date_range[1]
                resources.perioddetail_id = int(request.POST['perioddetail'])
                resources.typeresource_id = int(request.POST['typeresource'])
                resources.web_address = request.POST['web_address']
                resources.desc = request.POST['desc']
                resources.save()
            elif action == 'search_matters':
                data = [{'id': '', 'text': '--------------'}]
                period = request.POST['period']
                if len(period):
                    for det in PeriodDetail.objects.filter(period_id=period, contract__teacher__user=request.user):
                        data.append({
                            'id': det.id,
                            'text': 'Nombre: {} / Nivel: {}'.format(det.matter.name, det.matter.get_level_display())
                        })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Recurso'
        context['action'] = 'edit'
        return context


class ResourcesTeacherDeleteView(PermissionMixin, DeleteView):
    model = Resources
    template_name = 'resources/teacher/delete.html'
    success_url = reverse_lazy('resources_teacher_list')
    permission_required = 'delete_resources'

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
