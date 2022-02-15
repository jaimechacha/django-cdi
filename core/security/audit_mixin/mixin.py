from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str


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