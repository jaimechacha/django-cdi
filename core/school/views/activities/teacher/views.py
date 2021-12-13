import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.reports.forms import ReportForm
from core.school.forms import Activities, ActivitiesForm, PeriodDetail, Qualifications, Period
from core.security.mixins import PermissionMixin


class ActivitiesTeacherListView(PermissionMixin, FormView):
    form_class = ReportForm
    template_name = 'activities/teacher/list.html'
    permission_required = 'view_activities'

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
                search = Activities.objects.filter(perioddetail__contract__teacher__user=request.user)
                if len(period):
                    search = search.filter(perioddetail__period__id=period)
                for d in search:
                    data.append(d.toJSON())
            elif action == 'search_notes':
                data = []
                for d in Qualifications.objects.filter(activities_id=request.POST['id']):
                    data.append(d.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('activities_teacher_create')
        context['title'] = 'Listado de Actividades'
        return context


class ActivitiesTeacherCreateView(PermissionMixin, CreateView):
    model = Activities
    template_name = 'activities/teacher/create.html'
    form_class = ActivitiesForm
    success_url = reverse_lazy('activities_teacher_list')
    permission_required = 'add_activities'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = ActivitiesForm(initial={
            'period': Period.objects.filter(state=True).order_by('-id')[0]
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                date_range = request.POST['date_range'].split(' - ')
                activities = Activities()
                activities.name = request.POST['name']
                activities.start_date = date_range[0]
                activities.end_date = date_range[1]
                activities.perioddetail_id = int(request.POST['perioddetail'])
                activities.typeactivity_id = int(request.POST['typeactivity'])
                activities.web_address = request.POST['web_address']
                activities.desc = request.POST['desc']
                if 'rubric-clear' in request.POST:
                    activities.remove_rubric()
                if 'rubric' in request.FILES:
                    activities.rubric = request.FILES['rubric']
                activities.save()
            elif action == 'search_matters':
                data = [{'id': '', 'text': '--------------'}]
                period = request.POST['period']
              
                
                if len(period):
                   
                    for det in PeriodDetail.objects.filter(period_id=period, contract__teacher__user=request.user):
                        print(det.id)
                        data.append({
                            'id': det.id,
                            #'text': 'Nombre: {} / Nivel: {}'.format(det.matter.name, det.matter.get_level_display())
                            'text': 'Nombre: {} / Nivel: {}'.format(det.matter.name, det.matter.level)
                        })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Actividad'
        context['action'] = 'add'
        return context


class ActivitiesTeacherUpdateView(PermissionMixin, UpdateView):
    model = Activities
    template_name = 'activities/teacher/create.html'
    form_class = ActivitiesForm
    success_url = reverse_lazy('activities_teacher_list')
    permission_required = 'change_activities'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ActivitiesForm(instance=instance, initial={
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
                activities = self.object
                activities.name = request.POST['name']
                activities.start_date = date_range[0]
                activities.end_date = date_range[1]
                activities.perioddetail_id = int(request.POST['perioddetail'])
                activities.typeactivity_id = int(request.POST['typeactivity'])
                activities.web_address = request.POST['web_address']
                activities.desc = request.POST['desc']
                if 'rubric' in request.FILES:
                    activities.rubric = request.FILES['rubric']
                activities.save()
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
        context['title'] = 'Edición de una Actividad'
        context['action'] = 'edit'
        return context


class ActivitiesTeacherDeleteView(PermissionMixin, DeleteView):
    model = Activities
    template_name = 'activities/teacher/delete.html'
    success_url = reverse_lazy('activities_teacher_list')
    permission_required = 'delete_activities'

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


class ActivitiesTeacherQualifyView(UpdateView):
    model = Activities
    form_class = ActivitiesForm
    template_name = 'activities/teacher/qualify.html'
    #reaalizar un metodo o accion que al crear una actividad todos los estudientes se guarden una calificacion con cero
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        print('-------')
        return super().dispatch(request, *args, **kwargs)

    def get_homework(self):
        data = []
        for i in self.object.qualifications_set.all():
            data.append(i.toJSON())
            print(i.toJSON())
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'qualify':
                with transaction.atomic():
                    activitiesjson = json.loads(request.POST['activities'])
                    for p in activitiesjson['homework']:
                        calif = Qualifications.objects.get(pk=p['id'])
                        calif.note = float(p['note'])
                        calif.comment = p['comment']
                        calif.state = True
                        calif.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Calificación de Actividades'
        context['instance'] = self.get_object()
        context['homework'] = self.get_homework()
        return context
