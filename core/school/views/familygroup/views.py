import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.school.forms import Family, FamilyGroup, FamilyForm, Student
from core.security.mixins import PermissionMixin


class FamilyListView(ListView):
    model = Family
    template_name = 'familygroup/list.html'
    # permission_required = 'view_matter'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('family_add')
        context['title'] = 'Composición del grupo familiar'
        context['tab_family'] = 'active'
        return context

    def get_queryset(self):
        user = self.request.user.id
        return Family.objects.filter(familygroup__student__user_id=user)


class FamilyCreateView(CreateView):
    model = Family
    template_name = 'familygroup/create.html'
    form_class = FamilyForm
    success_url = reverse_lazy('family_list')

    # permission_required = 'add_student'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Crear nuevo familiar'
        context['action'] = 'add'
        context['instance'] = None
        context['tab_family'] = 'active'
        return context

    def post(self, request, *args, **kwargs):
        user = int(request.user.id)
        try:
            student = Student.objects.get(user_id=user)
            with transaction.atomic():
                family = FamilyForm(request.POST)
                fam = family.save()

                fam_group = FamilyGroup(student=student, family=fam)
                fam_group.save()
            return redirect('family_list')
        except Exception as e:
            data = {'error': str(e)}
            print(data)
            # return HttpResponse(json.dumps(data), content_type='application/json')


class FamilyUpdateView(UpdateView):
    model = Family
    template_name = 'familygroup/create.html'
    form_class = FamilyForm
    success_url = reverse_lazy('family_list')
    # permission_required = 'change_material'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición del familiar'
        context['action'] = 'edit'
        context['tab_family'] = 'active'
        return context


class FamilyDeleteView(DeleteView):
    model = Family
    template_name = 'familygroup/delete.html'
    success_url = reverse_lazy('family_list')
    # permission_required = 'delete_entry'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        context['tab_family'] = 'active'
        return context

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            fam = self.get_object()
            with transaction.atomic():
                fg = FamilyGroup.objects.get(family_id=fam.id)
                fg.delete()
                fam.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

