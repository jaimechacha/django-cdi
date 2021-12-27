import json
import os
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from weasyprint import CSS, HTML

from config import settings
from core.reports.forms import ReportForm, Student
from core.school.models import Assistance, Company
from core.security.mixins import ModuleMixin


class StudentReportView(ModuleMixin, FormView):
    template_name = 'student_report/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_search_data(self):
        period = self.request.POST['period']
        course = self.request.POST['course']
        search = []
        if len(period) and len(course):
            search = Student.objects.filter(matriculation__period_id=period, matriculation__level_id=course)
        return search

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                for i in self.get_search_data():
                    data.append(i.toJSON())
            elif action == 'generate_pdf':
                context = {
                    'data': self.get_search_data(),
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Estudiantes'
                }
                template = get_template('student_report/pdf.html')
                html_template = template.render(context).encode(encoding="UTF-8")
                url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.3.1/css/bootstrap.min.css')
                pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
                    stylesheets=[CSS(url_css)], presentational_hints=True)
                return HttpResponse(pdf_file, content_type='application/pdf')
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Estudiantes'
        return context
