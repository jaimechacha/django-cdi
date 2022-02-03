import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from core.security.mixins import ModuleMixin
from core.school.forms import CompanyForm, Company


class CompanyUpdateView(ModuleMixin, UpdateView):
    template_name = 'company/create.html'
    form_class = CompanyForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                comp = self.get_object()
                comp.name = request.POST['name']
                comp.ruc = request.POST['ruc']
                comp.mobile = request.POST['mobile']
                comp.email = request.POST['email']
                comp.address = request.POST['address']
                if 'image-clear' in request.POST:
                    comp.remove_image()
                if 'image' in request.FILES:
                    comp.image = request.FILES['image']
                comp.mission = request.POST['mission']
                comp.vision = request.POST['vision']
                comp.about_us = request.POST['about_us']
                comp.desc = request.POST['desc']
                comp.coordinates = request.POST['coordinates']
                comp.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Información del CDI'
        context['action'] = 'edit'
        return context
