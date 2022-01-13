import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, ListView
from core.reports.forms import ReportForm
from core.school.forms import Activities, ActivitiesForm, NoteDetailsForm, PeriodDetail, Qualifications, Period, \
    Matriculation, NoteDetails, Scores, Matter, Cursos
from core.school.models import Punctuations, MatriculationDetail
from core.security.mixins import PermissionMixin


class NoteDetailsStudentMatterListView(FormView):
    form_class = ReportForm
    template_name = 'notedetails/student/list.html'

    # permission_required = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['matter'].queryset = Matter.objects.filter(
            level__matriculation__student__user=self.request.user
        )
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                period = request.POST.get('period', None)
                matter = request.POST.get('matter', None)
                search = Punctuations.objects.filter()
                if period and matter:
                    if MatriculationDetail.objects.filter(perioddetail__period_id=period,
                                                          matriculation__student__user=request.user).exists():
                        search = search.filter(
                            notedetails_id__perioddetail__period_id=period,
                            student__user=request.user,
                            notedetails__perioddetail__matter_id=matter
                        )
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
