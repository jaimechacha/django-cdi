from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView

from core.school.forms import StudentMedicalRecordForm, StudentMedicalRecord
from core.security.mixins import PermissionMixin


class StudentMedicalRecordCreateView(CreateView):
    model = StudentMedicalRecord
    template_name = 'medicalrecord/create.html'
    form_class = StudentMedicalRecordForm
    success_url = reverse_lazy('student_medrecord_create')
    # permission_required = 'add_student'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Ficha médica'
        context['action'] = 'add'
        context['instance'] = None
        context['tab_ficha'] = 'active'
        return context
