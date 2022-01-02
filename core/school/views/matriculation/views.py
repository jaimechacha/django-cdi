import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, UpdateView, DeleteView

from core.reports.forms import ReportForm
from core.school.forms import Matriculation, MatriculationForm, PeriodDetail, MatriculationDetail, Period, Cursos
from core.security.mixins import PermissionMixin


class MatriculationListView(PermissionMixin, FormView):
    template_name = 'matriculation/list.html'
    permission_required = 'view_matriculation'
    form_class = ReportForm

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
                matriculation = Matriculation.objects.filter()
                if len(period):
                    matriculation = matriculation.filter(matriculationdetail__perioddetail__period_id=period)
                for i in matriculation:
                    item = i.toJSON()
                    item['cant'] = i.matriculationdetail_set.all().count()
                    data.append(item)
            elif action == 'search_matters':
                data = []
                matriculation = Matriculation.objects.get(pk=request.POST['id'])
                for d in matriculation.matriculationdetail_set.all():
                    data.append(d.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('matriculation_create')
        context['title'] = 'Listado de Matriculas'
        return context


class MatriculationCreateView(PermissionMixin, CreateView):
    model = Matriculation
    template_name = 'matriculation/create.html'
    form_class = MatriculationForm
    success_url = reverse_lazy('matriculation_list')
    permission_required = 'add_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = MatriculationForm(initial={
            'period': Period.objects.filter(state=True).order_by('-id')[0]
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            period = request.POST.get('period', None)
            level = request.POST.get('level', None)
            if action == 'search_matters_period':
                data = []
                if len(period) and len(level):
                    for i in PeriodDetail.objects.filter(period_id=period, matter__level=level):
                        item = i.toJSON()
                        item['status'] = False
                        data.append(item)
            elif action == 'get_coupons':
                enroll_students = Matriculation.objects.filter(period_id=period, level=level).count()
                max_level_coupon = Cursos.objects.get(id=level).max_coupon
                available_coupons = max_level_coupon - enroll_students
                data['coupons'] = available_coupons
            elif action == 'add':
                with transaction.atomic():
                    # enroll_students = Matriculation.objects.filter(period_id=period, level=level).count()
                    # max_level_coupon = Cursos.objects.get(id=level).max_coupon
                    # if enroll_students == max_level_coupon:
                    #     raise AssertionError("No hay cupos disponibles para este nivel")

                    students = json.loads(request.POST['students'])
                    for s in students:
                        matriculation = Matriculation()
                        matriculation.student_id = s['id']
                        matriculation.period_id = s['period_id']
                        matriculation.level_id = s['level_id']
                        # matriculation.save()

                #     for i in json.loads(request.POST['matters']):
                #         det = MatriculationDetail()
                #         det.matriculation_id = matriculation.id
                #         det.perioddetail_id = int(i['id'])
                #         det.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Matricula'
        context['action'] = 'add'
        return context


class MatriculationUpdateView(PermissionMixin, UpdateView):
    model = Matriculation
    template_name = 'matriculation/create.html'
    form_class = MatriculationForm
    success_url = reverse_lazy('matriculation_list')
    permission_required = 'change_matriculation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = MatriculationForm(instance=self.object)
        form.fields['student'].widget.attrs['disabled'] = True
        form.fields['period'].widget.attrs['disabled'] = True
        form.fields['level'].widget.attrs['disabled'] = True
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search_matters_period':
                data = []
                period = request.POST['period']
                level = request.POST['level']
                if len(period) and len(level):
                    for i in PeriodDetail.objects.filter(period_id=period, matter__level=level):
                        item = i.toJSON()
                        status = MatriculationDetail.objects.filter(matriculation_id=self.get_object().id,
                                                                    perioddetail_id=i.id).exists()
                        item['status'] = 1 if status else 0
                        data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    matriculation = self.get_object()
                    matriculation.student_id = request.POST['student']
                    matriculation.period_id = request.POST['period']
                    matriculation.level = request.POST['level']
                    matriculation.save()
                    matriculation.matriculationdetail_set.all().delete()
                    for i in json.loads(request.POST['matters']):
                        det = MatriculationDetail()
                        det.matriculation_id = matriculation.id
                        det.perioddetail_id = int(i['id'])
                        det.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Matricula'
        context['action'] = 'edit'
        return context


class MatriculationDeleteView(PermissionMixin, DeleteView):
    model = Matriculation
    template_name = 'matriculation/delete.html'
    success_url = reverse_lazy('matriculation_list')
    permission_required = 'delete_matriculation'

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
