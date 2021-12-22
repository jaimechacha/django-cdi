import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView

from config import settings
from core.school.forms import TeacherForm, User, Teacher, Parish, CVitae, CVitaeForm
from core.security.mixins import ModuleMixin, PermissionMixin


class TeacherListView(PermissionMixin, TemplateView):
    template_name = 'teacher/list.html'
    permission_required = 'view_teacher'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Teacher.objects.filter():
                    data.append(i.toJSON())
            elif action == 'search_cvitae':
                data = []
                for det in CVitae.objects.filter(teacher_id=request.POST['id']):
                    data.append(det.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('teacher_create')
        context['title'] = 'Listado de Profesores'
        return context


class TeacherCreateView(PermissionMixin, CreateView):
    model = Teacher
    template_name = 'teacher/create.html'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')
    permission_required = 'add_teacher'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Teacher.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    teacher = Teacher()
                    teacher.user_id = user.id
                    teacher.gender = request.POST['gender']
                    teacher.mobile = request.POST['mobile']
                    teacher.phone = request.POST['phone']
                    teacher.address = request.POST['address']
                    teacher.birthdate = request.POST['birthdate']
                    teacher.parish_id = int(request.POST['parish'])

                    teacher.reference = request.POST['reference']

                    teacher.nationality = request.POST['nationality']
                    teacher.age = int(request.POST['age']) if request.POST['age'] else None
                    teacher.ethnicity = request.POST['ethnicity']
                    teacher.religion = request.POST['religion']
                    teacher.civil_status = request.POST['civil_status']
                    teacher.blood_group = request.POST['blood_group']
                    teacher.disability = request.POST['disability']
                    teacher.disability_type = request.POST['disability_type']
                    teacher.cat_illnesses = request.POST['cat_illnesses']
                    teacher.cat_illnesses_desc = request.POST['cat_illnesses_desc']
                    if 'croquis' in request.FILES:
                        teacher.croquis = request.FILES['croquis']
                    if 'basic_services_payment' in request.FILES:
                        teacher.basic_services_payment = request.FILES['basic_services_payment']
                    if 'ci_doc' in request.FILES:
                        teacher.ci_doc = request.FILES['ci_doc']
                    if 'commitment_act' in request.FILES:
                        teacher.commitment_act = request.FILES['commitment_act']
                    if 'contract' in request.FILES:
                        teacher.contract = request.FILES['contract']
                    teacher.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('teacher'))
                    user.groups.add(group)

                    cvitaejson = json.loads(request.POST['cvitae'])
                    for det in cvitaejson:
                        cvitae = CVitae()
                        cvitae.teacher_id = teacher.id
                        cvitae.start_date = det['start_date']
                        cvitae.end_date = det['end_date']
                        cvitae.typecvitae_id = int(det['typecvitae']['id'])
                        cvitae.name = det['name']
                        cvitae.details = det['details']
                        cvitae.save()
            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Profesor'
        context['action'] = 'add'
        context['cvitae'] = []
        context['instance'] = None
        context['frmCVitae'] = CVitaeForm()
        return context


class TeacherDeleteView(PermissionMixin, DeleteView):
    model = Teacher
    template_name = 'teacher/delete.html'
    success_url = reverse_lazy('teacher_list')
    permission_required = 'delete_teacher'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                user = instance.user
                instance.delete()
                user.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teacher/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Información del docente'
        return context


class GenericUpdateTeacher(UpdateView):
    model = Teacher
    form_class = TeacherForm
    title = ''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.teacher

    def get_cvitae(self):
        data = []
        try:
            instance = self.get_object()
            for det in instance.cvitae_set.all():
                data.append(det.toJSON())
        except:
            pass
        return json.dumps(data)

    def get_form(self, form_class=None):
        instance = self.object
        form = TeacherForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        if instance.parish:
            form.fields['parish'].queryset = Parish.objects.filter(id=instance.parish.id)
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Teacher.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    teacher = instance
                    teacher.user_id = user.id
                    teacher.gender = request.POST['gender']
                    teacher.mobile = request.POST['mobile']
                    teacher.phone = request.POST['phone']
                    teacher.address = request.POST['address']
                    teacher.birthdate = request.POST['birthdate']
                    teacher.parish_id = int(request.POST['parish'])
                    teacher.reference = request.POST['reference']

                    teacher.nationality = request.POST['nationality']
                    teacher.age = int(request.POST['age']) if request.POST['age'] else None
                    teacher.ethnicity = request.POST['ethnicity']
                    teacher.religion = request.POST['religion']
                    teacher.civil_status = request.POST['civil_status']
                    teacher.blood_group = request.POST['blood_group']
                    teacher.disability = request.POST['disability']
                    teacher.disability_type = request.POST['disability_type']
                    teacher.cat_illnesses = request.POST['cat_illnesses']
                    teacher.cat_illnesses_desc = request.POST['cat_illnesses_desc']
                    if 'croquis' in request.FILES:
                        teacher.croquis = request.FILES['croquis']
                    if 'basic_services_payment' in request.FILES:
                        teacher.basic_services_payment = request.FILES['basic_services_payment']
                    if 'ci_doc' in request.FILES:
                        teacher.ci_doc = request.FILES['ci_doc']
                    if 'commitment_act' in request.FILES:
                        teacher.commitment_act = request.FILES['commitment_act']
                    if 'contract' in request.FILES:
                        teacher.contract = request.FILES['contract']
                    teacher.save()

                    teacher.cvitae_set.all().delete()
                    cvitaejson = json.loads(request.POST['cvitae'])

                    for det in cvitaejson:
                        cvitae = CVitae()
                        cvitae.teacher_id = teacher.id
                        cvitae.start_date = det['start_date']
                        cvitae.end_date = det['end_date']
                        cvitae.typecvitae_id = int(det['typecvitae']['id'])
                        cvitae.name = det['name']
                        cvitae.details = det['details']
                        cvitae.save()

            elif action == 'search_parish':
                data = []
                term = request.POST['term']
                for i in Parish.objects.filter(name__icontains=term)[0:10]:
                    item = {'id': i.id, 'text': i.__str__(), 'data': i.toJSON()}
                    data.append(item)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = self.title
        context['action'] = 'edit'
        context['instance'] = self.object
        context['frmCVitae'] = CVitaeForm()
        context['cvitae'] = self.get_cvitae()
        return context


class TeacherUpdateProfileView(ModuleMixin, GenericUpdateTeacher):
    title = 'Edición del perfil'
    template_name = 'teacher/profile.html'
    success_url = reverse_lazy('dashboard')


class TeacherUpdateView(PermissionMixin, GenericUpdateTeacher):
    title = 'Edición de un profesor'
    template_name = 'teacher/create.html'
    success_url = reverse_lazy('teacher_list')
    permission_required = 'change_teacher'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.get(pk=pk)
