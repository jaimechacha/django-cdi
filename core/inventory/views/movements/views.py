import json

from django.http import HttpResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.inventory.forms import MaterialMovementsForm
from core.inventory.models import EntryMaterial, OutputMaterial


class MaterialMovements(FormView):
    template_name = 'movements/list.html'
    form_class = MaterialMovementsForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de movimientos'
        return context

    def get_filter_data(self):
        data = []
        material = self.request.POST.get('material', None)
        start_date = self.request.POST.get('start_date', None)
        end_date = self.request.POST.get('end_date', None)
        user = self.request.POST.get('user', None)

        if material and start_date and end_date and user:
            for ent in EntryMaterial.objects.filter(
                    # ~Q(entry__employee_id=user),
                    entry__employee_id=user,
                    material_id=material,
                    entry__date_entry__range=[start_date, end_date]):
                data.append(ent.to_json_movements())
            for out in OutputMaterial.objects.filter(
                    # ~Q(output__teacher__user_id=user),
                    output__teacher__user_id=user,
                    material_id=material,
                    output__date_output__range=[start_date, end_date]):
                data.append(out.to_json_movements())
        elif material:
            for ent in EntryMaterial.objects.filter(
                    material_id=material,
                    entry__date_entry__range=[start_date, end_date]):
                data.append(ent.to_json_movements())
            for out in OutputMaterial.objects.filter(
                    material_id=material,
                    output__date_output__range=[start_date, end_date]):
                data.append(out.to_json_movements())
            return data
        elif user:
            for ent in EntryMaterial.objects.filter(entry__employee_id=user):
                data.append(ent.to_json_movements())
            for out in OutputMaterial.objects.filter(output__teacher__user_id=user):
                data.append(out.to_json_movements())
            return data
        else:
            for ent in EntryMaterial.objects.all():
                data.append(ent.to_json_movements())
            for out in OutputMaterial.objects.all():
                data.append(out.to_json_movements())
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'get_data':
                data = self.get_filter_data()
            else:
                data['error'] = 'No ha selecionado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
