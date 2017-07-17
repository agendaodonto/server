from rest_framework.serializers import ModelSerializer

from app.schedule.models.patient import Patient
from app.schedule.serializers.clinic import ClinicListSerializer


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'last_name', 'sex', 'phone', 'clinic')


class PatientListSerializer(PatientSerializer):
    clinic = ClinicListSerializer()
