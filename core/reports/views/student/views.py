import json
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from xhtml2pdf import pisa

from core.school.models import Company
from core.security.mixins import ModuleMixin
from core.reports.forms import ReportForm, Student, Cursos, Period
from core.reports.utils import link_callback_report


class StudentReportView(ModuleMixin, FormView):
    template_name = 'student_report/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_search_data(self):
        period = self.request.POST.get('period', None)
        course = self.request.POST.get('course', None)
        search = []
        if period and course:
            search = Student.objects.filter(matriculation__period_id=period, matriculation__level_id=course)
            period = Period.objects.get(id=period)
            course = Cursos.objects.get(id=course)
        return search, period, course

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                students, _, _ = self.get_search_data()
                for i in students:
                    data.append(i.toJSON())
            elif action == 'generate_pdf':
                students, period, level = self.get_search_data()
                context = {
                    'data': students,
                    'period': period,
                    'level': level,
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Estudiantes'
                }
                template = get_template('student_report/pdf.html')
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
        context['title'] = 'Reporte de Estudiantes'
        return context
