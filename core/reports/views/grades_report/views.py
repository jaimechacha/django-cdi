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
from core.reports.forms import ReportForm, Student, Teacher, Cursos, NoteDetails
from core.school.models import Company
from core.security.mixins import ModuleMixin


class GradesReportView(ModuleMixin, FormView):
    template_name = 'grades_report/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_search_data(self):
        course = self.request.POST['course']
        period = self.request.POST['period']
        search = []
        if len(period):
            search = Teacher.objects.filter(contracts__perioddetail__period_id=period)
        if len(course):
            search = Teacher.objects.filter(contracts__perioddetail__matter__level_id=course)
        return search

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                for i in self.get_search_data():
                    data.append(i.toJSON())
            elif action == 'search_activities':
                data = []
                matter = self.request.POST['matter']
                if len(matter):
                    search = NoteDetails.objects.filter(perioddetail__matter_id=matter)
                    for i in search:
                        data.append(i.toJSON())
            elif action == 'generate_pdf':
                context = {
                    'data': self.get_search_data(),
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Docentes'
                }
                template = get_template('teachers_report/pdf.html')
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
        context['title'] = 'Reporte de notas'
        context['act'] = []
        return context
