import base64
import os
from datetime import datetime

from PIL import Image
from django.db import models
from django.forms import model_to_dict

from config import settings
from core.school.choices import months, course_level, horary, gender_person
from core.user.models import User


class Company(models.Model):
    name = models.CharField(verbose_name='Compañia', max_length=50, unique=True)
    ruc = models.CharField(verbose_name='Ruc', max_length=13, unique=True)
    mobile = models.CharField(verbose_name='Teléfono', max_length=10, unique=True)
    email = models.CharField(verbose_name='Correo Electrónico', max_length=50, unique=True)
    address = models.CharField(verbose_name='Dirección', max_length=255)
    image = models.ImageField(verbose_name='Logo', upload_to='company/%Y/%m/%d', null=True, blank=True)
    mission = models.CharField(verbose_name='Misión', max_length=1000)
    vision = models.CharField(verbose_name='Visión', max_length=1000)
    about_us = models.CharField(verbose_name='Quienes Somos', max_length=1000)
    desc = models.CharField(verbose_name='Descripción', max_length=1000)
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def get_latitude(self):
        return self.coordinates.split(',')[0].replace(',', '.')

    def get_longitude(self):
        return self.coordinates.split(',')[1].replace(',', '.')

    def toJSON(self):
        item = model_to_dict(self, exclude=['iva'])
        item['image'] = self.get_image()
        return item

    def get_base64_encoded_image(self):
        try:
            image = base64.b64encode(open(self.image.path, 'rb').read()).decode('utf-8')
            type_image = Image.open(self.image.path).format.lower()
            return "data:image/{};base64,{}".format(type_image, image)
        except:
            pass
        return None

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Compañia'),
        )
        db_table = 'empresa'
        ordering = ['-id']


class Country(models.Model):
    code = models.CharField(max_length=4, verbose_name='Código', unique=True)
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        ordering = ['-id']


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='País')
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    code = models.CharField(max_length=4, verbose_name='Código', unique=True)

    def __str__(self):
        return 'País: {} / Provincia: {}'.format(self.country.name, self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['country'] = self.country.toJSON()
        return item

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['-id']


class Canton(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='Provincia')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return '{} / Cantón: {}'.format(self.province.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['province'] = self.province.toJSON()
        return item

    class Meta:
        verbose_name = 'Cantón'
        verbose_name_plural = 'Cantones'
        ordering = ['-id']


class Parish(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.PROTECT, verbose_name='Cantón')
    name = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return '{} / Parroquia: {}'.format(self.canton.__str__(), self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['canton'] = self.canton.toJSON()
        return item

    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'
        ordering = ['-id']


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parroquia')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['parish'] = self.parish.toJSON()
        return item

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['-id']


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10, choices=gender_person, default=gender_person[0][0], verbose_name='Sexo')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono convencional')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parroquia')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['parish'] = self.parish.toJSON()
        return item

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['-id']


class TypeCVitae(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Hoja de Vida'
        verbose_name_plural = 'Tipos de Hoja de Vida'
        ordering = ['id']


class CVitae(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Profesor')
    typecvitae = models.ForeignKey(TypeCVitae, on_delete=models.PROTECT, verbose_name='Tipo')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    details = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Detalles')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['teacher'])
        item['typecvitae'] = self.typecvitae.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Hoja de Vida'
        verbose_name_plural = 'Hojas de Vida'
        ordering = ['id']


class Job(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Puesto de Trabajo'
        verbose_name_plural = 'Puesto de Trabajos'
        ordering = ['id']


class ConferenceTheme(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tema de Conferencia'
        verbose_name_plural = 'Temas de Conferencias'
        ordering = ['id']


class Shifts(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['-id']


class Contracts(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Empleado')
    job = models.ForeignKey(Job, on_delete=models.PROTECT, verbose_name='Cargo')
    shifts = models.ForeignKey(Shifts, on_delete=models.PROTECT, verbose_name='Turno')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    base_salary = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Salario Base')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return '{} / {}'.format(self.teacher.user.get_full_name(), self.job.name)

    def nro(self):
        return format(self.id, '06d')

    def toJSON(self):
        item = model_to_dict(self)
        item['nro'] = format(self.id, '06d')
        item['base_salary'] = format(self.base_salary, '.2f')
        item['teacher'] = self.teacher.toJSON()
        item['shifts'] = self.shifts.toJSON()
        item['job'] = self.job.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['id']


class TypeEvent(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    economic_sanction = models.BooleanField(default=False, verbose_name='Sanción económica')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'
        ordering = ['id']


class Events(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT, verbose_name='Contrato')
    typeevent = models.ForeignKey(TypeEvent, on_delete=models.PROTECT, verbose_name='Tipo de Evento')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    start_time = models.TimeField(default=datetime.now, verbose_name='Hora de inicio')
    end_time = models.TimeField(default=datetime.now, verbose_name='Hora de finalización')
    desc = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Valor')
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.typeevent.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-id']


class Assistance(models.Model):
    date_joined = models.DateField(default=datetime.now)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fk_teacher')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fk_user')
    year = models.IntegerField()
    month = models.IntegerField(choices=months, default=0)
    day = models.IntegerField()
    desc = models.CharField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.get_month_display()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['month'] = {'id': self.month, 'name': self.get_month_display()}
        item['user'] = self.user.toJSON()
        return item

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        default_permissions = ()
        permissions = (
            ('view_assistance', 'Can view Asistencias'),
            ('add_assistance', 'Can add Asistencias'),
            ('delete_assistance', 'Can delete Asistencias'),
        )
        ordering = ['id']


class Cursos(models.Model):
    name = models.CharField(max_length=23, null= False, blank=False, verbose_name='Nombre')
    descrip = models.CharField(max_length=70, null= False, blank=False)
    #state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']


class Matter(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50)
    level = models.ForeignKey(Cursos, on_delete=models.PROTECT, max_length=30, verbose_name='Nivel')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    #def toJSON(self):
    #    item = model_to_dict(self)
    #    item['level'] = {'id': self.level, 'name': self.level.name()}
    #    return item

    def toJSON(self):
        item = model_to_dict(self)
        item['level'] = self.level.toJSON()
        return item

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['id']


class Conferences(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de conferencia')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT, verbose_name='Profesor')
    conferencetheme = models.ForeignKey(ConferenceTheme, on_delete=models.PROTECT, verbose_name='Tema de Conferencia')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['contract'] = self.contract.toJSON()
        item['conferencetheme'] = self.conferencetheme.toJSON()
        return item

    class Meta:
        verbose_name = 'Tema de Conferencia'
        verbose_name_plural = 'Temas de Conferencias'
        ordering = ['id']


class Period(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ['id']


class PeriodDetail(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT)
    matter = models.ForeignKey(Matter, on_delete=models.PROTECT)

    def __str__(self):
        return self.period.name

    def toJSON(self):
        item = model_to_dict(self)
        item['period'] = self.period.toJSON()
        item['contract'] = self.contract.toJSON()
        item['matter'] = self.matter.toJSON()
        return item

    class Meta:
        verbose_name = 'Periodo Detalle'
        verbose_name_plural = 'Periodos Detalles'
        ordering = ['id']


class Tutorials(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT, verbose_name='Profesor')
    horary = models.CharField(max_length=100, choices=horary, verbose_name='Horario')
    desc = models.CharField(max_length=500, verbose_name='Descripción')

    def __str__(self):
        return self.contract.teacher.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tutoría'
        verbose_name_plural = 'Tutorías'
        ordering = ['id']


class Matriculation(models.Model):
    date_joined = models.DateField(default=datetime.now)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    #level = models.CharField(choices=course_level, max_length=30)
    level = models.ForeignKey(Cursos, on_delete=models.PROTECT, max_length=30, verbose_name='Nivel')

    def __str__(self):
        return 'Alumno: {} / Número de cedula: {} /  Periodo: {}'.format(self.student.user.get_full_name(),
                                                                         self.student.user.dni,
                                                                         self.period.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['student'] = self.student.toJSON()
        item['period'] = self.period.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['level'] = self.level.toJSON()
        return item

    class Meta:
        verbose_name = 'Matriculación'
        verbose_name_plural = 'Matriculaciones'
        ordering = ['id']


class MatriculationDetail(models.Model):
    matriculation = models.ForeignKey(Matriculation, on_delete=models.PROTECT)
    perioddetail = models.ForeignKey(PeriodDetail, on_delete=models.PROTECT)

    def __str__(self):
        return self.matriculation.student.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        item['perioddetail'] = self.perioddetail.toJSON()
        return item

    class Meta:
        verbose_name = 'Matriculación Materia'
        verbose_name_plural = 'Matriculaciones Materias'
        ordering = ['id']


class PsychologicalOrientation(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    matriculation = models.ForeignKey(Matriculation, on_delete=models.PROTECT, verbose_name='Alumno')
    desc = models.CharField(max_length=5000, verbose_name='Detalles')

    def __str__(self):
        return self.desc

    def toJSON(self):
        item = model_to_dict(self)
        item['matriculation'] = self.matriculation.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Orientación Psicológica'
        verbose_name_plural = 'Orientaciones Psicológica'
        ordering = ['id']


class Breakfast(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Desayuno'
        verbose_name_plural = 'Desayunos'
        ordering = ['id']


class SchoolFeeding(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    breakfast = models.ForeignKey(Breakfast, on_delete=models.PROTECT, verbose_name='Tipo de colación')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='Estudiante')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.breakfast.name

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['student'] = self.student.toJSON()
        item['breakfast'] = self.breakfast.toJSON()
        item['desc'] = 'Ninguna' if self.desc is None else self.desc
        return item

    class Meta:
        verbose_name = 'Alimentación escolar'
        verbose_name_plural = 'Alimentación escolares'
        ordering = ['id']


class TypeResource(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Recurso'
        verbose_name_plural = 'Tipos de Recursos'
        ordering = ['id']


class Resources(models.Model):
    typeresource = models.ForeignKey(TypeResource, on_delete=models.PROTECT, verbose_name='Tipo de Recurso')
    perioddetail = models.ForeignKey(PeriodDetail, on_delete=models.PROTECT, verbose_name='Matería')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    web_address = models.CharField(max_length=200, verbose_name='Enlace')
    desc = models.CharField(max_length=1500, verbose_name='Descripción')

    def __str__(self):
        return self.web_address

    def toJSON(self):
        item = model_to_dict(self)
        item['typeresource'] = self.typeresource.toJSON()
        item['perioddetail'] = self.perioddetail.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['id']


class TypeActivity(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Actividad'
        verbose_name_plural = 'Tipos de Actividades'
        ordering = ['id']


class Activities(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    typeactivity = models.ForeignKey(TypeActivity, on_delete=models.PROTECT, verbose_name='Tipo de Actividad')
    perioddetail = models.ForeignKey(PeriodDetail, on_delete=models.PROTECT, verbose_name='Materia')
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    web_address = models.CharField(max_length=200, verbose_name='Enlace')
    rubric = models.ImageField(upload_to='activities/%Y/%m/%d', null=True, blank=True, verbose_name='Rubrica')
    punctuation = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    desc = models.CharField(max_length=1500, verbose_name='Descripción')
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.web_address

    def remove_rubric(self):
        try:
            if self.image:
                os.remove(self.rubric.path)
        except:
            pass
        finally:
            self.image = None

    def get_rubric(self):
        if self.rubric:
            return '{}{}'.format(settings.MEDIA_URL, self.rubric)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['typeactivity'] = self.typeactivity.toJSON()
        item['perioddetail'] = self.perioddetail.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['rubric'] = self.get_rubric()
        item['punctuation'] = format(self.punctuation, '.2f')
        return item

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['id']


class Qualifications(models.Model):
    activities = models.ForeignKey(Activities, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    archive = models.ImageField(upload_to='qualifications/%Y/%m/%d', null=True, blank=True)
    date_joined = models.DateField(default=datetime.now)
    note = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    comment = models.CharField(max_length=200, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.comment

    def get_archive(self):
        if self.archive:
            return '{}{}'.format(settings.MEDIA_URL, self.archive)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['archive'] = self.get_archive()
        item['activities'] = self.activities.toJSON()
        item['comment'] = '' if self.comment is None else self.comment
        item['student'] = self.student.toJSON()
        item['note'] = format(self.note, '.2f')
        return item

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering = ['id']


class NoteDetails(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    typeactivity = models.ForeignKey(TypeActivity, on_delete=models.PROTECT, verbose_name='Tipo de Actividad')
    perioddetail = models.ForeignKey(PeriodDetail, on_delete=models.PROTECT, verbose_name='Materia')
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    desc = models.CharField(max_length=1500, verbose_name='Descripción')
    state = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        item['typeactivity'] = self.typeactivity.toJSON()
        item['perioddetail'] = self.perioddetail.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['id']


class Scores(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')         
    score = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        item['score'] = format(self.score, '.2f')
        return item
    
    class Meta:
        verbose_name = 'RB Puntaje'
        verbose_name_plural = 'RB Puntajes'
        ordering = ['id']


class Punctuations(models.Model):
    notedetails = models.ForeignKey(NoteDetails, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    score = models.ForeignKey(Scores, on_delete=models.PROTECT)
    note = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    comment = models.CharField(max_length=200, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.comment
    
    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['notedetails'] = self.notedetails.toJSON()
        item['comment'] = '' if self.comment is None else self.comment
        item['student'] = self.student.toJSON()
        item['score'] = self.score.toJSON()
        item['note'] = format(self.note, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Puntaje'
        verbose_name_plural = 'Puntajes'
        ordering = ['id']

