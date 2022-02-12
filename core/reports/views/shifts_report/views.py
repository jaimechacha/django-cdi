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
from core.school.models import Contracts, Company
from core.security.mixins import ModuleMixin


class ShiftsReportView(ModuleMixin, FormView):
    template_name = 'shifts_report/report.html'
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
                shifts = self.request.POST['shifts']
                search = Contracts.objects.filter(state=True)
                if len(shifts):
                    search = search.filter(shifts_id=shifts)
                if len(start_date) and len(end_date):
                    search = search.filter(start_date__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            elif action == 'generate_pdf':
                start_date = self.request.POST['start_date']
                end_date = self.request.POST['end_date']
                shifts = self.request.POST['shifts']
                search = Contracts.objects.filter(state=True)
                if len(shifts):
                    search = search.filter(shifts_id=shifts)
                if len(start_date) and len(end_date):
                    search = search.filter(start_date__range=[start_date, end_date])
                context = {
                    'data': search,
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date(),
                    'title': 'Reporte de Turnos'
                }
                template = get_template('shifts_report/pdf.html')
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
        context['title'] = 'Reporte de Turnos'
        return context
