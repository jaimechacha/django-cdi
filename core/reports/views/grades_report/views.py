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
from core.reports.forms import ReportForm, Student, NoteDetails, Punctuations, Matter, Period, Cursos
from core.reports.utils import link_callback_report


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
            ).order_by('start_date')
        return data

    def search_students(self):
        data = []
        period = self.request.POST.get('period', None)
        level = self.request.POST.get('course', None)
        matter = self.request.POST.get('matter', None)
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']

        mat = Matter.objects.get(id=int(matter))

        if period and level and matter:
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
                ).order_by('notedetails__start_date')
                obj = {0: s.user.get_full_name()}
                for i, p in enumerate(punt):
                    obj[i + 1] = str(p.note)
                data.append(obj)
            period = Period.objects.get(id=period)
            level = Cursos.objects.get(id=level)
        return data, period, level, mat

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_activities':
                data = []
                for i in self.get_activities():
                    data.append(i.toJSON())
            elif action == 'search_students':
                students, _, _, _ = self.search_students()
                data = students
            elif action == 'search_materia':
                level = request.POST.get('level', None)
                data = []
                for m in Matter.objects.filter(level_id=int(level)).order_by('name')[0:10]:
                    data.append(m.toJSON())
            elif action == 'generate_pdf':
                students, period, lvl, matter = self.search_students()
                context = {
                    'activities': self.get_activities(),
                    'students': students,
                    'period': period,
                    'level': lvl,
                    'matter': matter,
                    'start_date': self.request.POST.get('start_date', None),
                    'end_date': self.request.POST.get('end_date', None),
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Notas'
                }
                template = get_template('grades_report/pdf.html')
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
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de notas'
        return context
