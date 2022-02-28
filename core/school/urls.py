from django.urls import path

from core.school.views.activities.student.views import ActivitiesStudentListView
from core.school.views.assistance.teacher.views import *
from core.school.views.assistance.student.views import *
from core.school.views.breakfast.views import *
from core.school.views.canton.views import *
from core.school.views.company.views import CompanyUpdateView
from core.school.views.conferences.views import *
from core.school.views.conferencetheme.views import *
from core.school.views.contracts.views import *
from core.school.views.country.views import *
from core.school.views.events.views import *
from core.school.views.job.views import *
from core.school.views.matriculation.views import *
from core.school.views.cursos.views import *
from core.school.views.matter.views import *
from core.school.views.parish.views import *
from core.school.views.period.views import *
from core.school.views.province.views import *
from core.school.views.psychologicalorientation.views import *
from core.school.views.resources.student.views import ResourcesStudentListView
from core.school.views.schoolfeeding.views import *
from core.school.views.shifts.views import *
from core.school.views.student.views import *
from core.school.views.teacher.views import *
from core.school.views.tutorials.views import *
from core.school.views.typeactivity.views import *
from core.school.views.typecvitae.views import *
from core.school.views.typeevent.views import *
from core.school.views.typeresource.views import *
from core.school.views.resources.teacher.views import *
from core.school.views.activities.teacher.views import *
from core.school.views.notedetails.teacher.views import *
from core.school.views.notedetails.student.views import *
from core.school.views.medicalrecord.views import *
from core.school.views.legalrepresentative.views import *
from core.school.views.familygroup.views import *

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # province
    path('province/', ProvinceListView.as_view(), name='province_list'),
    path('province/add/', ProvinceCreateView.as_view(), name='province_create'),
    path('province/update/<int:pk>/', ProvinceUpdateView.as_view(), name='province_update'),
    path('province/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete'),
    # canton
    path('canton/', CantonListView.as_view(), name='canton_list'),
    path('canton/add/', CantonCreateView.as_view(), name='canton_create'),
    path('canton/update/<int:pk>/', CantonUpdateView.as_view(), name='canton_update'),
    path('canton/delete/<int:pk>/', CantonDeleteView.as_view(), name='canton_delete'),
    # parish
    path('parish/', ParishListView.as_view(), name='parish_list'),
    path('parish/add/', ParishCreateView.as_view(), name='parish_create'),
    path('parish/update/<int:pk>/', ParishUpdateView.as_view(), name='parish_update'),
    path('parish/delete/<int:pk>/', ParishDeleteView.as_view(), name='parish_delete'),
    # country
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/add/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
    # student
    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/add/', StudentCreateView.as_view(), name='student_create'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/detail/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('student/update/profile/', StudentUpdateProfileView.as_view(), name='student_update_profile'),
    path('student/data/pdf/<int:pk>/', print_stud_data.as_view(), name='stud_print_pdf'),

    # job
    path('job/', JobListView.as_view(), name='job_list'),
    path('job/add/', JobCreateView.as_view(), name='job_create'),
    path('job/update/<int:pk>/', JobUpdateView.as_view(), name='job_update'),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name='job_delete'),
    # conferencetheme
    path('conference/theme/', ConferenceThemeListView.as_view(), name='conferencetheme_list'),
    path('conference/theme/add/', ConferenceThemeCreateView.as_view(), name='conferencetheme_create'),
    path('conference/theme/update/<int:pk>/', ConferenceThemeUpdateView.as_view(), name='conferencetheme_update'),
    path('conference/theme/delete/<int:pk>/', ConferenceThemeDeleteView.as_view(), name='conferencetheme_delete'),
    # shits
    path('shifts/', ShiftsListView.as_view(), name='shifts_list'),
    path('shifts/add/', ShiftsCreateView.as_view(), name='shifts_create'),
    path('shifts/update/<int:pk>/', ShiftsUpdateView.as_view(), name='shifts_update'),
    path('shifts/delete/<int:pk>/', ShiftsDeleteView.as_view(), name='shifts_delete'),
    # breakfast
    path('breakfast/', BreakfastListView.as_view(), name='breakfast_list'),
    path('breakfast/add/', BreakfastCreateView.as_view(), name='breakfast_create'),
    path('breakfast/update/<int:pk>/', BreakfastUpdateView.as_view(), name='breakfast_update'),
    path('breakfast/delete/<int:pk>/', BreakfastDeleteView.as_view(), name='breakfast_delete'),
    # typecvitae
    path('type/cvitae/', TypeCVitaeListView.as_view(), name='typecvitae_list'),
    path('type/cvitae/add/', TypeCVitaeCreateView.as_view(), name='typecvitae_create'),
    path('type/cvitae/update/<int:pk>/', TypeCVitaeUpdateView.as_view(), name='typecvitae_update'),
    path('type/cvitae/delete/<int:pk>/', TypeCVitaeDeleteView.as_view(), name='typecvitae_delete'),
    # typeactivity
    path('type/activity/', TypeActivityListView.as_view(), name='typeactivity_list'),
    path('type/activity/add/', TypeActivityCreateView.as_view(), name='typeactivity_create'),
    path('type/activity/update/<int:pk>/', TypeActivityUpdateView.as_view(), name='typeactivity_update'),
    path('type/activity/delete/<int:pk>/', TypeActivityDeleteView.as_view(), name='typeactivity_delete'),
    # typeevent
    path('type/event/', TypeEventListView.as_view(), name='typeevent_list'),
    path('type/event/add/', TypeEventCreateView.as_view(), name='typeevent_create'),
    path('type/event/update/<int:pk>/', TypeEventUpdateView.as_view(), name='typeevent_update'),
    path('type/event/delete/<int:pk>/', TypeEventDeleteView.as_view(), name='typeevent_delete'),
    # events
    path('events/', EventsListView.as_view(), name='events_list'),
    path('events/add/', EventsCreateView.as_view(), name='events_create'),
    path('events/update/<int:pk>/', EventsUpdateView.as_view(), name='events_update'),
    path('events/delete/<int:pk>/', EventsDeleteView.as_view(), name='events_delete'),
    # typeresource
    path('type/resource/', TypeResourceListView.as_view(), name='typeresource_list'),
    path('type/resource/add/', TypeResourceCreateView.as_view(), name='typeresource_create'),
    path('type/resource/update/<int:pk>/', TypeResourceUpdateView.as_view(), name='typeresource_update'),
    path('type/resource/delete/<int:pk>/', TypeResourceDeleteView.as_view(), name='typeresource_delete'),
    # Cursos
    path('cursos/', CursosListView.as_view(), name='cursos_list'),
    path('cursos/add/', CursosCreateView.as_view(), name='cursos_create'),
    path('cursos/update/<int:pk>/', CursosUpdateView.as_view(), name='cursos_update'),
    path('cursos/delete/<int:pk>/', CursosDeleteView.as_view(), name='cursos_delete'),
    # matter
    path('matter/', MatterListView.as_view(), name='matter_list'),
    path('matter/add/', MatterCreateView.as_view(), name='matter_create'),
    path('matter/update/<int:pk>/', MatterUpdateView.as_view(), name='matter_update'),
    path('matter/delete/<int:pk>/', MatterDeleteView.as_view(), name='matter_delete'),
    # teacher
    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/add/', TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('teacher/detail/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('teacher/delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('teacher/update/profile/', TeacherUpdateProfileView.as_view(), name='teacher_update_profile'),
    path('teacher/data/pdf/<int:pk>/', print_teacher_date.as_view(), name='techer_print_pdf'),

    # contracts
    path('contracts/', ContractsListView.as_view(), name='contracts_list'),
    path('contracts/add/', ContractsCreateView.as_view(), name='contracts_create'),
    path('contracts/update/<int:pk>/', ContractsUpdateView.as_view(), name='contracts_update'),
    path('contracts/delete/<int:pk>/', ContractsDeleteView.as_view(), name='contracts_delete'),
    # period
    path('period/', PeriodListView.as_view(), name='period_list'),
    path('period/add/', PeriodCreateView.as_view(), name='period_create'),
    path('period/update/<int:pk>/', PeriodUpdateView.as_view(), name='period_update'),
    path('period/delete/<int:pk>/', PeriodDeleteView.as_view(), name='period_delete'),
    path('period/assignment/teacher/<int:pk>/', PeriodAssignmentTeacherView.as_view(), name='period_assignment_teacher'),
    path('period/teacher/consult/', PeriodTeacherConsultView.as_view(), name='period_teacher_consult'),
    path('period/student/consult/', PeriodStudentConsultView.as_view(), name='period_student_consult'),
    # matriculation
    path('matriculation/', MatriculationListView.as_view(), name='matriculation_list'),
    path('matriculation/add/', MatriculationCreateView.as_view(), name='matriculation_create'),
    path('matriculation/update/<int:pk>/', MatriculationUpdateView.as_view(), name='matriculation_update'),
    path('matriculation/delete/<int:pk>/', MatriculationDeleteView.as_view(), name='matriculation_update'),
    # teacher
    path('assistance/teacher/', AssistanceTeacherListView.as_view(), name='assistance_teacher_list'),
    path('assistance/teacher/add/', AssistanceTeacherCreateView.as_view(), name='assistance_teacher_create'),
    path('assistance/teacher/delete/<str:start_date>/<str:end_date>/', AssistanceTeacherDeleteView.as_view(), name='assistance_teacher_delete'),
    # student assitance
    path('assistance/student/', AssistanceStudentListView.as_view(), name='assistance_student_list'),
    # tutorials
    path('tutorials/', TutorialsListView.as_view(), name='tutorials_list'),
    path('tutorials/add/', TutorialsCreateView.as_view(), name='tutorials_create'),
    path('tutorials/update/<int:pk>/', TutorialsUpdateView.as_view(), name='tutorials_update'),
    path('tutorials/delete/<int:pk>/', TutorialsDeleteView.as_view(), name='tutorials_delete'),
    path('tutorials/student/', TutorialsStudentListView.as_view(), name='tutorials_student'),
    # schoolfeeding
    path('schoolfeeding/', SchoolFeedingListView.as_view(), name='schoolfeeding_list'),
    path('schoolfeeding/add/', SchoolFeedingCreateView.as_view(), name='schoolfeeding_create'),
    path('schoolfeeding/update/<int:pk>/', SchoolFeedingUpdateView.as_view(), name='schoolfeeding_update'),
    path('schoolfeeding/delete/<int:pk>/', SchoolFeedingDeleteView.as_view(), name='schoolfeeding_delete'),
    # psychologicalorientation
    path('psychological/orientation/', PsychologicalOrientationListView.as_view(), name='psychologicalorientation_list'),
    path('psychological/orientation/add/', PsychologicalOrientationCreateView.as_view(), name='psychologicalorientation_create'),
    path('psychological/orientation/update/<int:pk>/', PsychologicalOrientationUpdateView.as_view(), name='psychologicalorientation_update'),
    path('psychological/orientation/delete/<int:pk>/', PsychologicalOrientationDeleteView.as_view(), name='psychologicalorientation_delete'),
    # resources/teacher
    path('resources/teacher/', ResourcesTeacherListView.as_view(), name='resources_teacher_list'),
    path('resources/teacher/add/', ResourcesTeacherCreateView.as_view(), name='resources_teacher_create'),
    path('resources/teacher/update/<int:pk>/', ResourcesTeacherUpdateView.as_view(), name='resources_teacher_update'),
    path('resources/teacher/delete/<int:pk>/', ResourcesTeacherDeleteView.as_view(), name='resources_teacher_delete'),
    path('resources/student/', ResourcesStudentListView.as_view(), name='resources_student_delete'),
    # activities/teacher
    path('activities/teacher/', ActivitiesTeacherListView.as_view(), name='activities_teacher_list'),
    path('activities/teacher/add/', ActivitiesTeacherCreateView.as_view(), name='activities_teacher_create'),
    path('activities/teacher/update/<int:pk>/', ActivitiesTeacherUpdateView.as_view(), name='activities_teacher_update'),
    path('activities/teacher/delete/<int:pk>/', ActivitiesTeacherDeleteView.as_view(), name='activities_teacher_delete'),
    path('activities/student/', ActivitiesStudentListView.as_view(), name='activities_student_list'),
    path('activities/teacher/qualify/<int:pk>/', ActivitiesTeacherQualifyView.as_view(), name='activities_teacher_qualify'),
    # conferences
    path('conferences/', ConferencesListView.as_view(), name='conferences_list'),
    path('conferences/add/', ConferencesCreateView.as_view(), name='conferences_create'),
    path('conferences/update/<int:pk>/', ConferencesUpdateView.as_view(), name='conferences_update'),
    path('conferences/delete/<int:pk>/', ConferencesDeleteView.as_view(), name='conferences_delete'),
    # notedetails/teacher
    path('notedetails/teacher_matter/', NoteDetailsTeacherMatterListView.as_view(), name='notedetails_teacher_matter'),
    path('notedetails/teacher/add/<int:pk>/', NoteDetailsTeacherCreateView.as_view(), name='notedetails_teacher_create'),
    path('notedetails/teacher/update/<int:pk>/', NoteDetailsTeacherUpdateView.as_view(), name='notedetails_teacher_update'),
    path('notedetails/teacher/puntuations/<int:pk>/', NotedetailsTeacherPuntuationsView.as_view(), name='notedetails_teacher_puntuatios'),
    path('notedetails/teacher/delete/<int:pk>/', NotedetailsTeacherDeleteView.as_view(), name='notedetails_teacher_delete'),
    # notedetails/student
    path('notedetails/student_matter/', NoteDetailsStudentMatterListView.as_view(), name='notedetails_student_matter'),
    # Student medical record
    path('student/medrecord/', StudentMedicalRecordListView.as_view(), name='student_medrecord'),
    path('student/medrecord/add/', StudentMedicalRecordCreateView.as_view(), name='student_medrecord_create'),
    path('student/medrecord/update/<int:pk>/', StudentMedicalRecordUpdateView.as_view(), name='student_medrecord_update'),
    # Legal representative
    path('student/representative/', LegalRepresentativeListView.as_view(), name='leg_representative'),
    path('student/representative/add/', LegalRepresentativeCreateView.as_view(), name='leg_representative_create'),
    path('student/representative/update/<int:pk>/', LegalRepresentativeUpdateView.as_view(), name='leg_representative_update'),
    # Family group
    path('student/family/', FamilyListView.as_view(), name='family_list'),
    path('student/family/add/', FamilyCreateView.as_view(), name='family_add'),
    path('student/family/update/<int:pk>/', FamilyUpdateView.as_view(), name='family_update'),
    path('student/family/delete/<int:pk>/', FamilyDeleteView.as_view(), name='family_delete'),
]
