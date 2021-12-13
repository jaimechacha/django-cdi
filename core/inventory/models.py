from django.conf import settings
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from core.school.models import Cursos, Teacher
from core.user.models import User


class Material(models.Model):
    name = models.CharField('Nombre', max_length=30, blank=True, null=True)
    description = models.TextField('Descripción', blank=True, null=True)
    image = models.ImageField('Imagen', upload_to='materials/%Y/%m/%d', null=True, blank=True)
    course = models.ForeignKey(Cursos, on_delete=models.PROTECT, verbose_name='Curso')

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['-id']

    def __str__(self):
        return '{} {}'.format(self.name, self.course)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['course'] = self.course.name
        item['value'] = '{} - {}'.format(self.name, self.course.name)
        return item


class Entry(models.Model):
    date_entry = models.DateField('Fecha de ingreso', default=datetime.now)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Responsable')

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return '{} {}'.format(self.employee.__str__(), self.date_entry)


class EntryMaterial(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.IntegerField('Cantidad', blank=True, null=True)

    class Meta:
        verbose_name = 'Entrada material'
        verbose_name_plural = 'Entrada de materiales'

    def __str__(self):
        return '{} {} {}'.format(self.entry.id, self.material.name, self.amount)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.name
        item['course'] = self.material.course.name
        return item


class Inventory(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    stock = models.IntegerField('Stock', blank=True, null=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return '{} - {}'.format(self.material.name, self.stock)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.toJSON()
        item['course'] = self.material.course.name
        item['value'] = '{} {}'.format(self.material.name, self.material.course.name)
        return item


class Output(models.Model):
    date_output = models.DateField('Fecha de salida', default=datetime.now)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Docente')

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return '{} {}'.format(self.teacher.__str__(), self.date_output)


class OutputMaterial(models.Model):
    output = models.ForeignKey(Output, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.IntegerField('Cantidad', blank=True, null=True)

    class Meta:
        verbose_name = 'Salida material'
        verbose_name_plural = 'Salida de materiales'

    def __str__(self):
        return '{} {} {}'.format(self.output.id, self.material.name, self.amount)

    def toJSON(self):
        item = model_to_dict(self)
        item['material'] = self.material.name
        item['course'] = self.material.course.name
        return item
