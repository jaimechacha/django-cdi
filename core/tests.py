from config.wsgi import *
from django.contrib.auth.models import Permission

from core.school.models import *
from core.security.models import *
from core.user.models import *

# company
dashboard = Dashboard()
dashboard.name = 'College Web'
dashboard.system_name = 'College Web'
dashboard.icon = 'fas fa-graduation-cap'
dashboard.layout = 1
dashboard.card = ' '
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.brand_logo = ''
dashboard.sidebar = 'sidebar-light-primary'
dashboard.save()

comp = Company()
comp.name = 'UE Marcel Laniado'
comp.ruc = '0928363993'
comp.mobile = '0979014551'
comp.email = 'uamarce@hotmail.com'
comp.address = 'Cdla.Dager, avda. tumbez y carchi'
comp.mission = 'Sin detalles'
comp.vision = 'Sin detalles'
comp.about_us = 'Sin detalles'
comp.desc = 'Sin detalles'
comp.iva = 0.12
comp.coordinates = '-2.2397839,-79.8966192'
comp.save()

module = Module()
module.name = 'Cambiar password'
module.url = '/user/admin/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/user/admin/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/school/teacher/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/school/student/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Tutorias'
module.url = '/school/tutorials/student/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las tutorias de los estudiantes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Asistencias'
module.url = '/school/assistance/teacher/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las asistencias de los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=Assistance._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Recursos'
module.url = '/school/resources/student/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-capsules'
module.description = 'Permite administrar los recursos para los estudiantes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Actividades'
module.url = '/school/activities/teacher/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-book'
module.description = 'Permite administrar las actividades para los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Actividades'
module.url = '/school/activities/student/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-book'
module.description = 'Permite administrar las actividades para los estudiantes'
module.save()
print('insertado {}'.format(module.name))

# module type
type = ModuleType()
type.name = 'Seguridad'
type.icon = 'fas fa-lock'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Info.Colegio'
module.url = '/school/company/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-building'
module.description = 'Permite administrar la información de la compañia'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for p in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for p in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Usuarios'
module.url = '/user/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los usuarios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Empleados'
type.icon = 'fas fa-school'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 2
module.name = 'Turnos'
module.url = '/school/shifts/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar los turnos de los docentes del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Shifts._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Tipos de CVitae'
module.url = '/school/type/cvitae/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-briefcase'
module.description = 'Permite administrar los tipos de curriculum vitae de los docentes'
module.save()
for p in Permission.objects.filter(content_type__model=TypeCVitae._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Eventos'
module.url = '/school/events/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-clock'
module.description = 'Permite administrar los eventos para los contratos'
module.save()
for p in Permission.objects.filter(content_type__model=Events._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Contratos'
module.url = '/school/contracts/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-signature'
module.description = 'Permite administrar los contratos de los empleados'
module.save()
for p in Permission.objects.filter(content_type__model=Contracts._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Profesor'
module.url = '/school/teacher/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chalkboard-teacher'
module.description = 'Permite administrar los profesores del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Teacher._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Tipos de Eventos'
module.url = '/school/type/event/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-week'
module.description = 'Permite administrar los tipos de eventos para los contratos'
module.save()
for p in Permission.objects.filter(content_type__model=TypeEvent._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Cargos'
module.url = '/school/job/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-address-card'
module.description = 'Permite administrar los cargos de los docentes del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Job._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Ubicación'
type.icon = 'fas fa-street-view'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 3
module.name = 'Paises'
module.url = '/user/country/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe-europe'
module.description = 'Permite administrar los paises'
module.save()
for p in Permission.objects.filter(content_type__model=Country._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Provincias'
module.url = '/user/province/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe'
module.description = 'Permite administrar las provincias del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Province._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Cantones'
module.url = '/user/canton/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-globe-americas'
module.description = 'Permite administrar los cantones del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Canton._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 3
module.name = 'Parroquias'
module.url = '/user/parish/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-search-location'
module.description = 'Permite administrar las parroquias del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Parish._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Gestión'
type.icon = 'fas fa-graduation-cap'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 4
module.name = 'Asignaturas'
module.url = '/school/matter/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-book-open'
module.description = 'Permite administrar las asignaturas del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Matter._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Tipos de Colación'
module.url = '/school/breakfast/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-bread-slice'
module.description = 'Permite administrar los tipos de desayuno del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Breakfast._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Tipos de Actividades'
module.url = '/school/type/activity/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-window-restore'
module.description = 'Permite administrar los tipos de actividades para las tareas'
module.save()
for p in Permission.objects.filter(content_type__model=TypeActivity._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Tipos de Recursos'
module.url = '/school/type/resource/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-boxes'
module.description = 'Permite administrar los tipos de recursos para las tareas'
module.save()
for p in Permission.objects.filter(content_type__model=TypeResource._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Temas de Conferencia'
module.url = '/school/conference/theme/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-microphone'
module.description = 'Permite administrar los temas de las conferencias'
module.save()
for p in Permission.objects.filter(content_type__model=ConferenceTheme._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Estudiantes'
module.url = '/school/student/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-graduate'
module.description = 'Permite administrar los estudiantes del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Student._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Periodos'
module.url = '/school/period/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-book'
module.description = 'Permite administrar los periodos del colegio'
module.save()
for p in Permission.objects.filter(content_type__model=Period._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Materias'
module.url = '/school/period/teacher/consult/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-book'
module.description = 'Permite administrar los periodos del colegio del docente'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Matriculación'
module.url = '/school/matriculation/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite administrar las matriculas de los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=Matriculation._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Tutorias'
module.moduletype_id = 4
module.url = '/school/tutorials/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las tutorias de los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=Tutorials._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Alimentación escolar'
module.url = '/school/schoolfeeding/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-utensils'
module.description = 'Permite administrar los eventos para los contratos'
module.save()
for p in Permission.objects.filter(content_type__model=SchoolFeeding._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Orientación Psicológica'
module.url = '/school/psychological/orientation/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-capsules'
module.description = 'Permite administrar las orientaciones psicológicas para los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=PsychologicalOrientation._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Recursos'
module.url = '/school/resources/teacher/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-capsules'
module.description = 'Permite administrar los recursos para los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=Resources._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Conferencias'
module.url = '/school/conferences/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-capsules'
module.description = 'Permite administrar las conferencias para los estudiantes'
module.save()
for p in Permission.objects.filter(content_type__model=Conferences._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Reportes'
type.icon = 'fas fa-chart-pie'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 5
module.name = 'Alimentación Escolar'
module.url = '/reports/school/feeding/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de la alimentación escolar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Orientación Psicológica'
module.url = '/reports/psychological/orientation/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de la orientación psicológica escolar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Conferencias'
module.url = '/reports/conferences/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las conferencias'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Turnos'
module.url = '/reports/shifts/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los turnos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Asistencia Est.'
module.url = '/reports/assistance/student/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las asistencias'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Asistencia Prof.'
module.url = '/reports/assistance/teacher/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las asistencias'
module.save()
print('insertado {}'.format(module.name))

# group
group = Group()
group.name = 'Administrador'
group.save()
print('insertado {}'.format(group.name))

for m in Module.objects.filter().exclude(
        url__in=['/school/assistance/teacher/',
                 '/school/period/teacher/consult/',
                 '/school/student/update/profile/',
                 '/school/teacher/update/profile/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for perm in m.permits.all():
        group.permissions.add(perm)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = perm.id
        grouppermission.save()

group = Group()
group.name = 'Profesor'
group.save()
print('insertado {}'.format(group.name))

for m in Module.objects.filter(
        url__in=[
            '/school/assistance/teacher/',
            '/school/period/teacher/consult/',
            '/user/admin/update/password/'
            '/school/teacher/update/profile/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

group = Group()
group.name = 'Estudiante'
group.save()
print('insertado {}'.format(group.name))

for m in Module.objects.filter(
        url__in=[
            '/school/student/update/profile/',
            '/school/tutorials/student/',
            '/user/admin/update/password/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

# user
u = User()
u.first_name = 'Jaime Enrique'
u.last_name = 'Santos Pizarro'
u.username = '0106319163'
u.dni = '0106319163'
u.email = 'ernques-clan1@outlook.com'
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.set_password('jaime1234')
u.save()
u.groups.add(Group.objects.get(pk=1))
