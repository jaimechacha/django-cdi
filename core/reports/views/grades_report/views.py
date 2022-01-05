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
from core.reports.forms import ReportForm, Student, Teacher, Cursos, NoteDetails, Punctuations, Matter, Period
from core.school.models import Company
from core.security.mixins import ModuleMixin


class GradesReportView(ModuleMixin, FormView):
    template_name = 'grades_report/report.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = ReportForm(initial={
            'period': Period.objects.filter(state=True).order_by('-id')[0]
        })
        return form

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_activities(self):
        data = []
        matter = self.request.POST['matter']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        if len(matter):
            data = NoteDetails.objects.filter(
                perioddetail__matter_id=matter,
                start_date__range=[start_date, end_date]
            )
        return data

    def search_students(self):
        data = []
        period = self.request.POST.get('period', None)
        level = self.request.POST.get('course', None)
        matter = self.request.POST.get('matter', None)
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        mat = Matter.objects.get(id=int(matter))

        students = Student.objects.filter(
            matriculation__period_id=int(period),
            matriculation__level_id=int(level),
            matriculation__level__matter=mat
        )
        for s in students:
            punt = Punctuations.objects.filter(
                student_id=s.id,
                notedetails__perioddetail__matter_id=int(matter),
                notedetails__start_date__range=[start_date, end_date]
            )
            obj = {0: s.user.get_full_name()}
            for i, p in enumerate(punt):
                obj[i + 1] = str(p.note)
            data.append(obj)
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_activities':
                data = []
                for i in self.get_activities():
                    data.append(i.toJSON())
            elif action == 'search_students':
                data = []
                data = self.search_students()
            elif action == 'search_materia':
                level = request.POST.get('level', None)
                data = []
                for m in Matter.objects.filter(level_id=int(level)).order_by('name')[0:10]:
                    data.append(m.toJSON())
            elif action == 'generate_pdf':
                context = {
                    'data': self.get_activities(),
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
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de notas'
        return context
