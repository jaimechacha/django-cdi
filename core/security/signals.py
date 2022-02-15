from .middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

list_models = ['Company', 'Country', 'Province', 'Canton',
               'Parish', 'Teacher', 'Student', 'LegalRepresentative',
               'StudentMedicalRecord', 'Family', 'FamilyGroup', 'TypeCVitae',
               'CVitae', 'Job', 'ConferenceTheme', 'Shifts',
               'Contracts', 'TypeEvent', 'Events', 'Assistance',
               'Cursos', 'Matter', 'Conferences', 'Period',
               'PeriodDetail', 'Tutorials', 'Matriculation', 'MatriculationDetail',
               'PsychologicalOrientation', 'Breakfast', 'SchoolFeeding', 'TypeResource',
               'Resources', 'TypeActivity', 'Activities', 'Qualifications', 'NoteDetails',
               'Scores', 'Punctuations', 'Web', 'Material',
               'Entry', 'EntryMaterial', 'Inventory', 'Output',
               'OutputMaterial', 'Dashboard', 'ModuleType', 'Module',
               'GroupModule', 'GroupPermission', 'DatabaseBackups', 'AccessUsers',
               'User']


@receiver(post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
    if sender.__name__ not in list_models:
        return

    user = get_user()

    if user is None:
        return
    if created:
        instance.save_addition(user)
    elif not raw:
        instance.save_edition(user)


@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
    if sender.__name__ not in list_models:
        return

    user = get_user()

    if user is None:
        return

    instance.save_deletion(user)


def get_user():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'user'):
        user = thread_local.user
        if user.is_anonymous:
            user = None
    else:
        user = None
    return user
