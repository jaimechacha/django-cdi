from datetime import datetime

from crum import get_current_request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str

from config import settings
from core.security.models import Module


class ModuleMixin(object):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request.session['module'] = None
        try:
            request.user.set_group_session()
            group_id = request.user.get_group_id_session()
            modules = Module.objects.filter(Q(moduletype__is_active=True) | Q(moduletype__isnull=True)).filter(
                groupmodule__group_id__in=[group_id], is_active=True, url=request.path, is_visible=True)
            if modules.exists():
                request.session['module'] = modules[0]
                return super().get(request, *args, **kwargs)
            else:
                messages.error(request, 'No tiene permiso para ingresar a este módulo')
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        except:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class PermissionMixin(object):
    permission_required = None

    def get_permits(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_last_url(self):
        request = get_current_request()
        if 'url_last' in request.session:
            return request.session['url_last']
        return settings.LOGIN_REDIRECT_URL

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request.session['module'] = None
        try:
            if 'group' in request.session:
                group = request.session['group']
                permits = self.get_permits()
                for p in permits:
                    if not group.grouppermission_set.filter(permission__codename=p).exists():
                        messages.error(request, 'No tiene permiso para ingresar a este módulo')
                        return HttpResponseRedirect(self.get_last_url())
                grouppermission = group.grouppermission_set.filter(permission__codename=permits[0])
                if grouppermission.exists():
                    request.session['url_last'] = request.path
                    request.session['module'] = grouppermission[0].module
                return super().get(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class AuditMixin(object):
    def save_log(self, user, message, action):
        log = LogEntry.objects.create(
            user_id=user.id,
            action_time=datetime.now(),
            content_type_id=ContentType.objects.get_for_model(self).id,
            object_id=self.id,
            object_repr=force_str(f'{self} ({ContentType.objects.get_for_model(self).model})'),
            action_flag=action,
            change_message=message,
        )

    def save_addition(self, user):
        self.save_log(user, 'Creación', ADDITION)

    def save_edition(self, user):
        self.save_log(user, 'Edición', CHANGE)

    def save_deletion(self, user):
        self.save_log(user, 'Eliminación', DELETION)
