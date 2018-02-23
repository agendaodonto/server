from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from app.schedule.models import Schedule, Patient, Dentist, Clinic


class ResetAPI(APIView):
    """
    Reset the application to a known state
    This was created for e2e testing purposes
    It should be disabled for production environment
    """
    permission_classes = (permissions.AllowAny,)
    dentists = []
    clinics = []
    patients = []
    schedules = []

    def get(self, request):
        self.clear_database()
        self.create_dentists()
        self.create_clinics()
        return Response('ok')

    def clear_database(self):
        Schedule.objects.all().delete()
        Patient.objects.all().delete()
        Clinic.objects.all().delete()
        Dentist.objects.all().delete()

    def create_dentists(self):
        """
        Creates 2 Dentists: Eduardo and Monica
        :return:
        """
        return [
            Dentist.objects.create_user('Eduardo', 'da Silva', 'eduardo@gmail.com', 'M', '1234', 'SP', 'hunter1'),
            Dentist.objects.create_user('Monica', 'Pinto', 'monica@gmail.com', 'F', '5555', 'MG', 'hunter2')
        ]

    def create_clinics(self):
        """
        Creates a clinic for each Dentist in the database
        :return:
        """
        for dentist in self.dentists:
            self.clinics.append(Clinic.objects.create(
                name='Clinica do %s' % dentist.get_short_name(),
                owner=dentist,
                dentists=[dentist],

            ))
