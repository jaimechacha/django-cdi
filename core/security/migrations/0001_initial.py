
import core.security.audit_mixin.mixin
import datetime
import django.contrib.admin.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('admin', '0003_logentry_add_action_flag_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('hour', models.TimeField(default=datetime.datetime.now)),
                ('localhost', models.TextField()),
                ('hostname', models.TextField(default='DESKTOP-6AC0JEF')),
            ],
            options={
                'verbose_name': 'Acceso del usuario',
                'verbose_name_plural': 'Accesos de los usuarios',
                'ordering': ['-id'],
                'permissions': (('view_accessusers', 'Can view Acceso del usuario'), ('delete_accessusers', 'Can delete Acceso del usuario')),
                'default_permissions': (),
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('image', models.ImageField(blank=True, null=True, upload_to='dashboard/%Y/%m/%d', verbose_name='Logo')),
                ('icon', models.CharField(max_length=500, verbose_name='Icono FontAwesome')),
                ('layout', models.IntegerField(blank=True, choices=[(1, 'Vertical'), (2, 'Horizontal')], default=1, null=True, verbose_name='Diseño')),
                ('card', models.CharField(choices=[(' ', 'clear'), ('card-primary', 'card-primary'), ('card-blue', 'card-blue'), ('card-indigo', 'card-indigo'), ('card-cyan', 'card-cyan'), ('card-danger', 'card-danger'), ('card-dark', 'card-dark'), ('card-fuchsia', 'card-fuchsia'), ('card-gray', 'card-gray'), ('card-gray-dark', 'card-gray-dark'), ('card-green', 'card-green'), ('card-info', 'card-info'), ('card-lime', 'card-lime'), ('card-maroon', 'card-maroon'), ('card-navy', 'card-navy'), ('card-olive', 'card-olive'), ('card-orange', 'card-orange'), ('card-outline', 'card-outline'), ('card-pink', 'card-pink'), ('card-purple', 'card-purple'), ('card-red', 'card-red'), ('card-secondary', 'card-secondary'), ('card-success', 'card-success'), ('card-teal', 'card-teal'), ('card-warning', 'card-warning'), ('card-white', 'card-white'), ('card-yellow', 'card-yellow'), ('card-outline card-primary', 'card-outline card-primary'), ('card-outline card-blue', 'card-outline card-blue'), ('card-outline card-indigo', 'card-outline card-indigo'), ('card-outline card-cyan', 'card-outline card-cyan'), ('card-outline card-danger', 'card-outline card-danger'), ('card-outline card-dark', 'card-outline card-dark'), ('card-outline card-fuchsia', 'card-outline card-fuchsia'), ('card-outline card-gray', 'card-outline card-gray'), ('card-outline card-gray-dark', 'card-outline card-gray-dark'), ('card-outline card-green', 'card-outline card-green'), ('card-outline card-info', 'card-outline card-info'), ('card-outline card-lime', 'card-outline card-lime'), ('card-outline card-maroon', 'card-outline card-maroon'), ('card-outline card-navy', 'card-outline card-navy'), ('card-outline card-olive', 'card-outline card-olive'), ('card-outline card-orange', 'card-outline color-paginaweb'), ('card-outline card-outline', 'card-outline card-outline'), ('card-outline card-pink', 'card-outline card-pink'), ('card-outline card-purple', 'card-outline card-purple'), ('card-outline card-red', 'card-outline card-red'), ('card-outline card-secondary', 'card-outline card-secondary'), ('card-outline card-success', 'card-outline card-success'), ('card-outline card-teal', 'card-outline card-teal'), ('card-outline card-warning', 'card-outline card-warning'), ('card-outline card-white', 'card-outline card-white'), ('card-outline card-yellow', 'card-outline card-yellow')], default=' ', max_length=50, verbose_name='Card')),
                ('navbar', models.CharField(choices=[('navbar-dark navbar-primary', 'navbar-primary'), ('navbar-dark navbar-secondary', 'navbar-secondary'), ('navbar-dark navbar-info', 'navbar-info'), ('navbar-dark navbar-success', 'navbar-success'), ('navbar-dark navbar-danger', 'navbar-danger'), ('navbar-dark navbar-indigo', 'navbar-indigo'), ('navbar-dark navbar-purple', 'navbar-purple'), ('navbar-dark navbar-pink', 'navbar-pink'), ('navbar-dark navbar-teal', 'navbar-teal'), ('navbar-expand navbar-dark', 'navbar-dark'), ('navbar-dark navbar-gray-dark', 'navbar-gray-dark'), ('navbar-dark navbar-gray', 'navbar-gray'), ('navbar-light', 'navbar-light'), ('navbar-light navbar-warning', 'navbar-warning'), ('navbar-light navbar-white', 'navbar-white'), ('navbar-light navbar-orange', 'navbar-color-paginaweb')], default='navbar-dark navbar-primary', max_length=50, verbose_name='Navbar')),
                ('brand_logo', models.CharField(choices=[('navbar-primary', 'navbar-primary'), ('navbar-secondary', 'navbar-secondary'), ('navbar-info', 'navbar-info'), ('navbar-success', 'navbar-success'), ('navbar-danger', 'navbar-danger'), ('navbar-indigo', 'navbar-indigo'), ('navbar-purple', 'navbar-purple'), ('navbar-pink', 'navbar-pink'), ('navbar-teal', 'navbar-teal'), ('navbar-cyan', 'navbar-cyan'), ('navbar-dark', 'navbar-dark'), ('navbar-gray-dark', 'navbar-gray-dark'), ('navbar-gray', 'navbar-gray'), ('navbar-light', 'navbar-light'), ('navbar-warning', 'navbar-warning'), ('navbar-white', 'navbar-white'), ('navbar-orange', 'navbar-orange'), (' ', 'clear')], default='navbar-primary', max_length=50, verbose_name='Brand Logo')),
                ('sidebar', models.CharField(choices=[('sidebar-dark-primary', 'sidebar-dark-primary'), ('sidebar-dark-warning', 'sidebar-dark-warning'), ('sidebar-dark-info', 'sidebar-dark-info'), ('sidebar-dark-danger', 'sidebar-dark-danger'), ('sidebar-dark-success', 'sidebar-dark-success'), ('sidebar-dark-indigo', 'sidebar-dark-indigo'), ('sidebar-dark-navy', 'sidebar-dark-navy'), ('sidebar-dark-purple', 'sidebar-dark-purple'), ('sidebar-dark-fuchsia', 'sidebar-dark-fuchsia'), ('sidebar-dark-pink', 'sidebar-dark-pink'), ('sidebar-dark-maroon', 'sidebar-dark-maroon'), ('sidebar-dark-orange', 'sidebar-dark-orange'), ('sidebar-dark-lime', 'sidebar-dark-lime'), ('sidebar-dark-teal', 'sidebar-dark-teal'), ('sidebar-dark-olive', 'sidebar-dark-olive'), ('sidebar-light-primary', 'sidebar-light-primary'), ('sidebar-light-warning', 'sidebar-light-warning'), ('sidebar-light-info', 'sidebar-light-info'), ('sidebar-light-danger', 'sidebar-light-danger'), ('sidebar-light-success', 'sidebar-light-success'), ('sidebar-light-indigo', 'sidebar-light-indigo'), ('sidebar-light-navy', 'sidebar-light-navy'), ('sidebar-light-purple', 'sidebar-light-purple'), ('sidebar-light-fuchsia', 'sidebar-light-fuchsia'), ('sidebar-light-pink', 'sidebar-light-pink'), ('sidebar-light-maroon', 'sidebar-light-maroon'), ('sidebar-light-orange', 'sidebar-light-orange'), ('sidebar-light-lime', 'sidebar-light-lime'), ('sidebar-light-teal', 'sidebar-light-teal'), ('sidebar-light-olive', 'sidebar-light-olive')], default='sidebar-dark-primary', max_length=50, verbose_name='Sidebar')),
            ],
            options={
                'verbose_name': 'Dashboard',
                'verbose_name_plural': 'Dashboards',
                'ordering': ['-id'],
                'permissions': (('view_dashboard', 'Can view Dashboard'),),
                'default_permissions': (),
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DatabaseBackups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('hour', models.TimeField(default=datetime.datetime.now)),
                ('localhost', models.CharField(blank=True, max_length=100, null=True)),
                ('hostname', models.TextField(blank=True, default='DESKTOP-6AC0JEF', null=True)),
                ('archive', models.FileField(upload_to='backup/%Y/%m/%d')),
            ],
            options={
                'verbose_name': 'Respaldos de BD',
                'verbose_name_plural': 'Respaldo de BD',
                'ordering': ['-id'],
                'permissions': (('view_databasebackups', 'Can view Respaldos de BD'), ('add_databasebackups', 'Can add Respaldos de BD'), ('delete_databasebackups', 'Can delete Respaldos de BD')),
                'default_permissions': (),
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ModuleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('icon', models.CharField(max_length=100, unique=True, verbose_name='Icono')),
                ('is_active', models.BooleanField(default=True, verbose_name='Estado')),
                ('position', models.IntegerField(blank=True, null=True, verbose_name='Posición')),
            ],
            options={
                'verbose_name': 'Tipo de Módulo',
                'verbose_name_plural': 'Tipos de Módulos',
                'ordering': ['-name'],
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('admin.logentry',),
            managers=[
                ('objects', django.contrib.admin.models.LogEntryManager()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, unique=True, verbose_name='Url')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción')),
                ('icon', models.CharField(blank=True, max_length=100, null=True, verbose_name='Icono')),
                ('image', models.ImageField(blank=True, null=True, upload_to='module/%Y/%m/%d', verbose_name='Imagen')),
                ('is_vertical', models.BooleanField(default=False, verbose_name='Vertical')),
                ('is_active', models.BooleanField(default=True, verbose_name='Estado')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('position', models.IntegerField(blank=True, null=True, verbose_name='Posición')),
                ('moduletype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='security.ModuleType', verbose_name='Tipo de Módulo')),
                ('permits', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='Permisos')),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['-name'],
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='security.Module')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Permission')),
            ],
            options={
                'verbose_name': 'Grupo Permiso',
                'verbose_name_plural': 'Grupos Permisos',
                'ordering': ['-id'],
                'default_permissions': (),
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GroupModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='security.Module')),
            ],
            options={
                'verbose_name': 'Grupo Módulo',
                'verbose_name_plural': 'Grupos Módulos',
                'ordering': ['-id'],
                'default_permissions': (),
            },
            bases=(core.security.audit_mixin.mixin.AuditMixin, models.Model),
        ),
    ]
