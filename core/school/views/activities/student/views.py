import json

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.reports.forms import ReportForm
from core.school.forms import Activities, MatriculationDetail, Qualifications
from core.security.mixins import ModuleMixin


class ActivitiesStudentListView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'activities/student/list.html'

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
                search = Activities.objects.filter()
                if len(period):
                    if MatriculationDetail.objects.filter(perioddetail__period_id=period,
                                                          matriculation__student__user=request.user).exists():
                        search = search.filter(perioddetail__period_id=period)
                        for d in search:
                            item = d.toJSON()
                            item['calif'] = {}
                            calif = Qualifications.objects.filter(activities_id=d.id,
                                                                  student_id=request.user.student.id)
                            if calif.exists():
                                item['calif'] = calif[0].toJSON()
                            data.append(item)
            elif action == 'upload_work':
                with transaction.atomic():
                    activities_id = int(request.POST['id'])
                    qualifications = Qualifications()
                    student_id = request.user.student.id
                    search = Qualifications.objects.filter(activities_id=activities_id, student_id=student_id)
                    if search.exists():
                        qualifications = search[0]
                    qualifications.student_id = student_id
                    qualifications.activities_id = activities_id
                    qualifications.archive = request.FILES['archive']
                    qualifications.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Actividades'
        return context
