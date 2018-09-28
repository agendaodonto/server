from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from app.schedule.views.clinic import ClinicDetail
from app.schedule.views.clinic import ClinicList, ClinicPatients
from app.schedule.views.dentist import DentistList, DentistDetail
from app.schedule.views.patient import PatientList, PatientDetail, PatientSchedule, PatientMessages
from app.schedule.views.schedule import ScheduleList, ScheduleDetail, ScheduleAttendance

urlpatterns = [
    # Schedules
    url(r'^schedules/$', ScheduleList.as_view(), name='schedules'),
    url(r'^schedules/(?P<pk>[0-9]+)/$', ScheduleDetail.as_view(), name='schedule-detail'),
    url(r'^schedules/attendance/$', ScheduleAttendance.as_view(), name='schedule-attendance'),

    # Patients
    url(r'^patients/$', PatientList.as_view(), name='patients'),
    url(r'^patients/(?P<pk>[0-9]+)/$', PatientDetail.as_view(), name='patient-detail'),
    url(r'^patients/(?P<pk>[0-9]+)/schedules/$', PatientSchedule.as_view(), name='patient-schedules'),
    url(r'^patients/(?P<pk>[0-9]+)/messages/$', PatientMessages.as_view(), name='patient-messages'),

    # Dentists
    url(r'^dentists/$', DentistList.as_view(), name='dentists'),
    url(r'^dentists/me/$', DentistDetail.as_view(), name='dentist-detail'),

    # Clinics
    url(r'^clinics/$', ClinicList.as_view(), name='clinics'),
    url(r'^clinics/(?P<pk>[0-9]+)/$', ClinicDetail.as_view(), name='clinic-detail'),
    url(r'^clinics/(?P<pk>[0-9]+)/patients/$', ClinicPatients.as_view(), name='clinic-patients'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
