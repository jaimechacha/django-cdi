from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from core.school.forms import LegalRepresentative, LegalRepresentativeForm, Student
from core.security.mixins import PermissionMixin


class LegalRepresentativeListView(ListView):
    model = LegalRepresentative
    template_name = 'legalrepresentative/detail.html'
    # permission_required = 'view_matter'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('leg_representative_create')
        context['title'] = 'Representante Legal'
        context['tab_representative'] = 'active'
        return context

    def get_queryset(self):
        user = self.request.user.id
        return LegalRepresentative.objects.filter(student__user_id=user)[0:1]


class LegalRepresentativeCreateView(CreateView):
    model = LegalRepresentative
    template_name = 'legalrepresentative/create.html'
    form_class = LegalRepresentativeForm
    success_url = reverse_lazy('leg_representative_create')
    # permission_required = 'add_student'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Representante legal'
        context['action'] = 'add'
        context['instance'] = None
        context['tab_representative'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        try:
            user = int(request.user.id)
            legal_form = LegalRepresentativeForm(request.POST.copy(), request.FILES)

            if request.user.groups.filter(name='Estudi').exists():
                student = Student.objects.get(user_id=user)
                legal_form.data['student'] = student.id
                legal_form.save()
                return redirect('leg_representative')
            elif request.user.groups.filter(name='Administrador').exists():
                legal_form.save()
                return redirect('leg_representative_create')
        except Exception as e:
            data = {'error': str(e)}
            print(data)
        return redirect('student_list')


class LegalRepresentativeUpdateView(UpdateView):
    model = LegalRepresentative
    template_name = 'legalrepresentative/create.html'
    form_class = LegalRepresentativeForm
    success_url = reverse_lazy('leg_representative')

    # permission_required = 'change_material'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de datos del representante'
        context['action'] = 'edit'
        context['instance'] = self.get_object()
        context['tab_representative'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        try:
            user = int(request.user.id)
            student = Student.objects.get(user_id=user)
            legal_form = LegalRepresentativeForm(
                request.POST.copy(),
                request.FILES,
                instance=self.get_object()
            )
            legal_form.data['student'] = student.id
            legal_form.save()
        except Exception as e:
            data = {'error': str(e)}
            print(data)
        return redirect('leg_representative')
