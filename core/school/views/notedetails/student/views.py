import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, ListView
from core.reports.forms import ReportForm
from core.school.forms import Activities, ActivitiesForm, NoteDetailsForm, PeriodDetail, Qualifications, Period, \
    Matriculation, NoteDetails, Scores
from core.school.models import Punctuations, MatriculationDetail
from core.security.mixins import PermissionMixin


class NoteDetailsStudentMatterListView(FormView):
    form_class = ReportForm
    template_name = 'notedetails/student/list.html'

    # permission_required = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                period = request.POST['period']
                search = Punctuations.objects.filter()
                if len(period):
                    if MatriculationDetail.objects.filter(perioddetail__period_id=period,
                                                          matriculation__student__user=request.user).exists():
                        search = search.filter(notedetails_id__perioddetail__period_id=period,
                                               student__user=request.user)
                        for d in search:
                            item = d.toJSON()
                            item['calif'] = {}
                            calif = Punctuations.objects.filter(notedetails_id=d.id,
                                                                student_id=request.user.student.id)
                            if calif.exists():
                                item['calif'] = calif[0].toJSON()
                            data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Calificaciones por Periodos'
        return context
