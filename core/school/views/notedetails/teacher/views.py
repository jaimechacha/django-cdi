import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, ListView

from core.reports.forms import ReportForm
from core.school.forms import Activities, ActivitiesForm, NoteDetailsForm, PeriodDetail, Qualifications, Period, Matriculation, NoteDetails, Scores
from core.school.models import Punctuations
from core.security.mixins import PermissionMixin

class NoteDetailsTeacherMatterListView(FormView):
    form_class = ReportForm
    template_name = 'notedetails/teacher/consult_period_teacher.html'
    #permission_required = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_period':
                data = []
                period = request.POST['period']
                if len(period):
                    for i in PeriodDetail.objects.filter(period_id=period, contract__teacher__user=request.user):
                        data.append(i.toJSON())
            elif action == 'search_students':
                data = []
                for i in Matriculation.objects.filter(matriculationdetail__perioddetail_id=request.POST['id'],
                                                      matriculationdetail__perioddetail__contract__teacher__user=request.user):
                    data.append(i.toJSON())
            elif action == 'search_notedetails':                
                data = []
                for i in NoteDetails.objects.filter(perioddetail_id=request.POST['id'],
                                                    perioddetail__matter_id=request.POST['matter_id'],
                                                    perioddetail__contract__teacher__user=request.user):
                    data.append(i.toJSON())
            elif action == 'search_punctuations':                
                data = []
                for d in Punctuations.objects.filter(notedetails_id=request.POST['id']):
                    data.append(d.toJSON())                 
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
    
    def get_homework(self):
        data = []       
        for i in Punctuations.objects.filter(notedetails__perioddetail_id=11,
                                                    notedetails__perioddetail__matter_id=1,
                                                    notedetails__perioddetail__contract__teacher__user=2):
                    data.append(i.toJSON())
        return json.dumps(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Materias por Periodos'
        context['homework'] = self.get_homework()
        return context

class NoteDetailsTeacherCreateView(FormView):
    model = NoteDetails
    template_name = 'notedetails/teacher/create.html'
    form_class = NoteDetailsForm
    success_url = reverse_lazy('notedetails_teacher_matter')
    #permission_required = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    instance = self.kwargs['pk']
                    date_range = request.POST['date_range'].split(' - ')
                    notedetails = NoteDetails()
                    notedetails.name = request.POST['name']
                    notedetails.start_date = date_range[0]
                    notedetails.end_date = date_range[1]
                    notedetails.perioddetail_id = int(instance)
                    notedetails.typeactivity_id = int(request.POST['typeactivity'])
                    notedetails.desc = request.POST['desc']
                    notedetails.save()
                    
                    for i in Matriculation.objects.filter(matriculationdetail__perioddetail_id=instance,
                                                        matriculationdetail__perioddetail__contract__teacher__user=request.user):
                        puntuations = Punctuations()
                        puntuations.note= int(1)
                                                
                        score = Scores.objects.get(score = float(1))
                        puntuations.score_id = score.id
                        
                        puntuations.student_id = i.student.id
                        puntuations.notedetails_id = notedetails.id
                        puntuations.save()                                                     
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #instance = Period.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'Registro de Actividad'
        context['score'] = NoteDetailsForm()
        context['list_url'] = 'javascript: history.go(-1)'
        context['action'] = 'add'
        return context

class NoteDetailsTeacherUpdateView(UpdateView):
    model = NoteDetails
    template_name = 'notedetails/teacher/create.html'
    form_class = NoteDetailsForm
    #success_url = reverse_lazy('')
    #permission_required = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':               
                date_range = request.POST['date_range'].split(' - ')
                notedetails = self.object
                notedetails.name = request.POST['name']
                notedetails.start_date = date_range[0]
                notedetails.end_date = date_range[1]               
                notedetails.typeactivity_id = int(request.POST['typeactivity'])
                notedetails.desc = request.POST['desc']
                notedetails.save()                                                                        
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = 'javascript: history.go(-1)'
        context['title'] = 'Edición de Actividad'
        context['action'] = 'edit'
        return context

class NotedetailsTeacherDeleteView(DeleteView):
    model = NoteDetails
    template_name = 'notedetails/teacher/delete.html'
    #success_url = reverse_lazy('')
    #permission_required = ''

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
        context['list_url'] = 'javascript: history.go(-1)'
        return context


class NotedetailsTeacherPuntuationsView(UpdateView):
    model = NoteDetails
    form_class = NoteDetailsForm
    template_name = 'notedetails/teacher/puntuations.html'
    success_url = reverse_lazy('notedetails_teacher_matter')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_homework(self):
        data = []            
        for i in self.object.punctuations_set.all():
            data.append(i.toJSON())           
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'punctuation':
                print(request.POST['form_data'])
                with transaction.atomic():
                    punctuationjson = json.loads(request.POST['notedetails'])
                    for p in punctuationjson['homework']:
                        calif = Punctuations.objects.get(pk=p['id'])
                        calif.note = float(p['note'])
    
                        note = float(p['note'])
                        score = Scores.objects.get(score=round(note, 0))
                        calif.score_id = score.id
                        
                        calif.comment = p['comment']
                        calif.state = True
                        calif.save()                        
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Calificaciones'
        context['list_url'] = 'javascript: history.go(-1)'
        context['instance'] = self.get_object()
        context['homework'] = self.get_homework()
        return context
