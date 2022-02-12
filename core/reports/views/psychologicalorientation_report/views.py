import json
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from xhtml2pdf import pisa

from core.reports.forms import ReportForm
from core.reports.utils import link_callback_report
from core.school.models import PsychologicalOrientation, Company
from core.security.mixins import ModuleMixin


class PsychologicalOrientationReportView(ModuleMixin, FormView):
    template_name = 'psychologicalorientation_report/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = self.request.POST['start_date']
                end_date = self.request.POST['end_date']
                student = self.request.POST['student']
                search = PsychologicalOrientation.objects.filter()
                if len(student):
                    search = search.filter(matriculation__student_id=student)
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            elif action == 'generate_pdf':
                start_date = self.request.POST['start_date']
                end_date = self.request.POST['end_date']
                student = self.request.POST['student']
                search = PsychologicalOrientation.objects.filter()
                if len(student):
                    search = search.filter(matriculation__student_id=student)
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                context = {
                    'data': search,
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Orientación Psicológica'
                }
                template = get_template('psychologicalorientation_report/pdf.html')
                html_template = template.render(context).encode(encoding="UTF-8")
                response = HttpResponse(content_type='application/pdf')
                pisa_status = pisa.CreatePDF(
                    html_template,
                    dest=response,
                    link_callback=link_callback_report
                )
                return response
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Orientación Psicológica'
        return context
