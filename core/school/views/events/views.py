import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.school.forms import EventsForm, Events, TypeEvent
from core.security.mixins import  PermissionMixin


class EventsListView(PermissionMixin, ListView):
    model = Events
    template_name = 'events/list.html'
    permission_required = 'view_events'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('events_create')
        context['title'] = 'Listado de Eventos'
        return context


class EventsCreateView(PermissionMixin, CreateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'add_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                events = Events()
                events.contract_id = request.POST['contract']
                events.typeevent_id = request.POST['typeevent']
                events.start_date = request.POST['start_date']
                events.end_date = request.POST['end_date']
                events.start_time = request.POST['start_time']
                events.end_time = request.POST['end_time']
                events.desc = request.POST['desc']
                if events.typeevent.economic_sanction:
                    events.valor = float(request.POST['valor'])
                events.save()
            elif action == 'search_typeevent':
                data = TypeEvent.objects.get(pk=request.POST['id']).toJSON()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Evento'
        context['action'] = 'add'
        return context


class EventsUpdateView(PermissionMixin, UpdateView):
    model = Events
    template_name = 'events/create.html'
    form_class = EventsForm
    success_url = reverse_lazy('events_list')
    permission_required = 'change_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        date_permit = '{} {} - {} {}'.format(instance.start_date.strftime('%Y-%m-%d'),
                                             instance.start_time.strftime('%H:%m'),
                                             instance.end_date.strftime('%Y-%m-%d'),
                                             instance.end_time.strftime('%H:%m'),
                                             )
        form = EventsForm(instance=instance, initial={
            'date_permit': date_permit
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                events = self.object
                events.contract_id = request.POST['contract']
                events.typeevent_id = request.POST['typeevent']
                events.start_date = request.POST['start_date']
                events.end_date = request.POST['end_date']
                events.start_time = request.POST['start_time']
                events.end_time = request.POST['end_time']
                events.desc = request.POST['desc']
                if events.typeevent.economic_sanction:
                    events.valor = float(request.POST['valor'])
                events.save()
            elif action == 'search_typeevent':
                data = TypeEvent.objects.get(pk=request.POST['id']).toJSON()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Evento'
        context['action'] = 'edit'
        return context


class EventsDeleteView(PermissionMixin, DeleteView):
    model = Events
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events_list')
    permission_required = 'delete_events'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
