import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from core.school.forms import StudentMedicalRecordForm, StudentMedicalRecord, Student
from core.security.mixins import PermissionMixin


class StudentMedicalRecordListView(ListView):
    model = StudentMedicalRecord
    template_name = 'medicalrecord/detail.html'
    # permission_required = 'view_matter'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('family_add')
        context['title'] = 'Ficha médica '
        context['tab_medical'] = 'active'
        return context

    def get_queryset(self):
        user = self.request.user.id
        return StudentMedicalRecord.objects.filter(student__user_id=user)[0:1]


class StudentMedicalRecordCreateView(CreateView):
    model = StudentMedicalRecord
    template_name = 'medicalrecord/create.html'
    form_class = StudentMedicalRecordForm
    success_url = reverse_lazy('student_medrecord')
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
        context['tab_medical'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        try:
            user = int(request.user.id)
            student = Student.objects.get(user_id=user)
            med_record = StudentMedicalRecordForm(request.POST.copy(), request.FILES)
            med_record.data['student'] = student.id
            med_record.save()
            return redirect('student_medrecord')
        except Exception as e:
            data = {'error': str(e)}
            print(data)
            # return HttpResponse(json.dumps(data), content_type='application/json')


class StudentMedicalRecordUpdateView(UpdateView):
    model = StudentMedicalRecord
    template_name = 'medicalrecord/create.html'
    form_class = StudentMedicalRecordForm
    success_url = reverse_lazy('student_medrecord')
    # permission_required = 'change_material'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de ficha médica'
        context['action'] = 'edit'
        context['instance'] = self.get_object()
        context['tab_medical'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        try:
            user = int(request.user.id)
            student = Student.objects.get(user_id=user)
            med_record = StudentMedicalRecordForm(request.POST.copy(), request.FILES, instance=self.get_object())
            med_record.data['student'] = student.id
            med_record.save()
            return redirect('student_medrecord')
        except Exception as e:
            data = {'error': str(e)}
            print(data)
