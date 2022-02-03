from django.db import models
from datetime import datetime
import base64
import os
from ckeditor.fields import RichTextField


from PIL import Image
from django.db import models
from django.forms import model_to_dict

from config import settings
# Create your models here.


class Web(models.Model):
    name = models.CharField(verbose_name='Centro infantil', max_length=50, unique=True)
    ruc = models.CharField(verbose_name='Ruc', max_length=13, unique=True)
    mobile = models.CharField(verbose_name='Teléfono', max_length=10, unique=True)
    email = models.CharField(verbose_name='Correo Electrónico', max_length=50, unique=True)
    address = models.CharField(verbose_name='Dirección', max_length=255)
    image = models.ImageField(verbose_name='Imagen Menu', upload_to='company/%Y/%m/%d', null=True, blank=True)
    image_about = models.ImageField(verbose_name='Imagen Nosotros', upload_to='company/%Y/%m/%d', null=True, blank=True, default='')
    mission = models.CharField(verbose_name='Misión', max_length=1000)
    vision = models.CharField(verbose_name='Visión', max_length=1000)
    about_us = RichTextField(null=True, blank=True)
    desc = models.CharField(verbose_name='Descripción', max_length=1000)
    coordinates = models.CharField(verbose_name='Coordenadas', max_length=50)
    servicios_text = models.CharField(verbose_name='Servicios', max_length=1000, default='')
    docentes_text = models.CharField(verbose_name='Edades', max_length=1000, default='')
    infraestructura_text = models.CharField(verbose_name='Horarios', max_length=1000, default='')
    block1 = models.CharField(verbose_name='Criterios de los niños', max_length=1000, default='')
    block2 = models.CharField(verbose_name='Grupos de trabajo', max_length=1000, default='')
    block3 = models.CharField(verbose_name='Tarifas y pagos', max_length=1000, default='')

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

    def get_image_about(self):
        if self.image_about:
            return '{}{}'.format(settings.MEDIA_URL, self.image_about)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def remove_image_about(self):
        try:
            if self.image_about:
                os.remove(self.image_about.path)
        except:
            pass
        finally:
            self.image_about = None

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
        verbose_name = 'Web'
        verbose_name_plural = 'Webs'
        default_permissions = ()
        permissions = (
            ('view_web', 'Can view Web'),
        )
        db_table = 'web'
        ordering = ['-id']
