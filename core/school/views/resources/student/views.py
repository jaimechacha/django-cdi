import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.reports.forms import ReportForm, MatriculationDetail
from core.school.forms import Resources
from core.security.mixins import ModuleMixin


class ResourcesStudentListView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'resources/student/list.html'

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
                search = Resources.objects.filter()
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
        context['title'] = 'Listado de Recursos'
        return context
