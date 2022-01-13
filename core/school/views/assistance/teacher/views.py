import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, TemplateView

from core.school.forms import Assistance, AssistanceForm, Matriculation
from core.security.mixins import PermissionMixin


class AssistanceTeacherListView(PermissionMixin, FormView):
    form_class = AssistanceForm
    template_name = 'assistance/list.html'
    permission_required = 'view_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search':
                data = []
                start_date = request.POST.get('start_date', datetime.now().date().strftime('%Y-%m-%d'))
                end_date = request.POST.get('end_date', datetime.now().date().strftime('%Y-%m-%d'))
                if len(start_date) and len(end_date):
                    for a in Assistance.objects.filter(date_joined__range=[start_date, end_date], is_teacher=False, teacher_id=request.user.id):
                        data.append(a.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assistance_teacher_create')
        context['title'] = 'Listado de Asistencias'
        return context


class AssistanceTeacherCreateView(PermissionMixin, CreateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_teacher_list')
    permission_required = 'add_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            obj = self.request.POST['obj'].strip()
            data['valid'] = True
            if Assistance.objects.filter(date_joined=obj, teacher_id=self.request.user.id):
                data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    assistances = json.loads(request.POST['items'])
                    #y = request.POST['yest']
                    date_joined = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')

                    a = Assistance()
                    a.date_joined = date_joined
                    a.year = date_joined.year
                    a.month = date_joined.month
                    a.day = date_joined.day
                    a.state = True
                    a.user_id = request.user.id
                    a.teacher_id = request.user.id
                    a.is_teacher = True
                    a.save()

                    for i in assistances:
                        a = Assistance()
                        a.user_id = int(i['user']['id'])
                        a.teacher_id = request.user.id
                        a.date_joined = date_joined
                        a.year = date_joined.year
                        a.month = date_joined.month
                        a.day = date_joined.day
                        a.desc = i['desc']
                        a.state = i['state']
                        a.save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'generate_assistance':
                data = []
                period = request.POST['period']
                if len(period):
                    for i in Matriculation.objects.filter(period_id=period):
                        if i.matriculationdetail_set.filter(perioddetail__contract__teacher__user=request.user):
                            item = i.student.toJSON()
                            item['state'] = 0
                            item['desc'] = ''
                            data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Asistencia'
        context['action'] = 'add'
        return context


class AssistanceTeacherDeleteView(PermissionMixin, TemplateView):
    model = Assistance
    template_name = 'assistance/delete.html'
    success_url = reverse_lazy('assistance_teacher_list')
    permission_required = 'delete_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = self.kwargs['start_date']
            end_date = self.kwargs['end_date']
            Assistance.objects.filter(date_joined__range=[start_date, end_date]).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        context['dates'] = self.kwargs
        return context
