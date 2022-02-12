import json
import os
from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from xhtml2pdf import pisa

from config import settings
from core.reports.forms import ReportForm, Teacher, Cursos, Period
from core.school.models import Company
from core.security.mixins import ModuleMixin


class TeachersReportView(ModuleMixin, FormView):
    template_name = 'teachers_report/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def link_callback(self, uri, rel):
        s_url = settings.STATIC_URL
        s_root = settings.STATIC_ROOT
        m_url = settings.MEDIA_URL
        m_root = settings.MEDIA_ROOT
        if uri.startswith(m_url):
            path = os.path.join(m_root, uri.replace(m_url, ""))
        elif uri.startswith(s_url):
            path = os.path.join(s_root, uri.replace(s_url, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (s_url, m_url)
            )
        return path

    def get_search_data(self):
        period = self.request.POST.get('period', None)
        course = self.request.POST.get('course', None)
        search = []
        if period:
            search = Teacher.objects.filter(contracts__perioddetail__period_id=period)
            period = Period.objects.get(id=period)
        if course:
            search = Teacher.objects.filter(contracts__perioddetail__matter__level_id=course)
            course = Cursos.objects.get(id=course)
        return search, period, course

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                teachers, _, _ = self.get_search_data()
                for i in teachers:
                    data.append(i.toJSON())
            elif action == 'generate_pdf':
                teachers, period, level = self.get_search_data()
                context = {
                    'data': teachers,
                    'period': period,
                    'level': level,
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Docentes'
                }
                template = get_template('teachers_report/pdf.html')
                html_template = template.render(context).encode(encoding="UTF-8")
                response = HttpResponse(content_type='application/pdf')
                pisa_status = pisa.CreatePDF(
                    html_template,
                    dest=response,
                    link_callback=self.link_callback
                )
                return response
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Docentes'
        return context
