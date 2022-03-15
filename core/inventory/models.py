from django.conf import settings
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from core.school.models import Cursos, Teacher
from core.user.models import User
from core.security.audit_mixin.mixin import AuditMixin


class Bodega(AuditMixin, models.Model):
    name = models.CharField('Nombre', max_length=30, blank=True, null=True)
    description = models.TextField('Descripción', blank=True, null=True)
    fecha_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['id']


class Material(AuditMixin, models.Model):
    name = models.CharField('Nombre', max_length=30, blank=True, null=True)
    description = models.TextField('Descripción', blank=True, null=True)
    image = models.ImageField('Imagen', upload_to='materials/%Y/%m/%d', null=True, blank=True)
    fecha_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['-id']

    def __str__(self):
        return '{}'.format(self.name)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['value'] = self.name
        return item


def generate_entry_num_doc():
    last_entry = Entry.objects.all().order_by('id').last()
    if not last_entry:
        return 'E001'
    num_doc = last_entry.num_doc
    num_doc_int = int(num_doc.split('E')[-1]) + 1
    new_num_doc = f'E00{num_doc_int}'
    return new_num_doc


class Entry(AuditMixin, models.Model):
    num_doc = models.CharField('Nº de documento', null=True, blank=True, max_length=30, default=generate_entry_num_doc)
    date_entry = models.DateField('Fecha de ingreso', default=datetime.now)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Responsable')
    fecha_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{} {}'.format(self.employee.__str__(), self.date_entry)


class EntryMaterial(AuditMixin, models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.IntegerField('Cantidad', blank=True, null=True)
    fecha_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrada material'
        verbose_name_plural = 'Entrada de materiales'

    def __str__(self):
        return '{} {} {}'.format(self.entry.id, self.material.name, self.amount)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.name
        item['description'] = self.material.description
        return item

    def to_json_movements(self):
        item = {
            'id_material': self.material.id,
            'material': self.material.name,
            'date': str(self.entry.date_entry),
            'amount_entry': self.amount,
            'amount_output': '',
            'employee_teacher': self.entry.employee.get_full_name(),
            'num_doc': self.entry.num_doc
        }
        return item


class Inventory(AuditMixin, models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    stock = models.IntegerField('Stock', blank=True, null=True)
    fecha_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return '{} - {}'.format(self.material.name, self.stock)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.toJSON()
        item['value'] = '{}'.format(self.material.name)
        return item


def generate_output_num_doc():
    last_output = Output.objects.all().order_by('id').last()
    if not last_output:
        return 'S001'
    num_doc = last_output.num_doc
    num_doc_int = int(num_doc.split('S')[-1]) + 1
    new_num_doc = f'S00{ num_doc_int }'
    return new_num_doc


class Output(AuditMixin, models.Model):
    num_doc = models.CharField('Nº de documento', null=True, blank=True, max_length=30, default=generate_output_num_doc)
    date_output = models.DateField('Fecha de salida', default=datetime.now)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Docente')
    fecha_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return '{} {}'.format(self.teacher.__str__(), self.date_output)


class OutputMaterial(AuditMixin, models.Model):
    output = models.ForeignKey(Output, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.IntegerField('Cantidad', blank=True, null=True)
    fecha_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Salida material'
        verbose_name_plural = 'Salida de materiales'

    def __str__(self):
        return '{} {} {}'.format(self.output.id, self.material.name, self.amount)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.name
        item['mat_id'] = self.material.id
        item['description'] = self.material.description
        return item

    def to_json_movements(self):
        item = {
            'id_material': self.material.id,
            'material': self.material.name,
            'date': str(self.output.date_output),
            'amount_entry': '',
            'amount_output': self.amount,
            'employee_teacher': self.output.teacher.user.get_full_name(),
            'num_doc': self.output.num_doc,
        }
        return item
