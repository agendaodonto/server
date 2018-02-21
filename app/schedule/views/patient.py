from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework import permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from app.schedule.models import Schedule, Message
from app.schedule.models.patient import Patient
from app.schedule.serializers.message import MessageSerializer
from app.schedule.serializers.patient import PatientSerializer, PatientListSerializer
from app.schedule.serializers.schedule import ScheduleSerializer


class PatientFilter(FilterSet):
    name = CharFilter(name='name', lookup_expr='icontains')
    last_name = CharFilter(name='last_name', lookup_expr='icontains')
    phone = CharFilter(name='phone', lookup_expr='icontains')
    full_name = CharFilter(name='full_name', method='search_by_full_name')

    def search_by_full_name(self, qs, name, value):
        for term in value.split():
            qs = qs.filter(Q(name__icontains=term) | Q(last_name__icontains=term))
        return qs

    class Meta:
        model = Patient
        fields = ['name', 'last_name', 'phone']


class PatientList(ListCreateAPIView):
    """
    Lista de pacientes
    """
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = PatientFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientListSerializer
        else:
            return PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(
            Q(clinic__dentists__pk=self.request.user.pk) |
            Q(clinic__owner=self.request.user)
        ).distinct()


class PatientDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes do paciente
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientListSerializer
        else:
            return PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(
            Q(clinic__dentists__pk=self.request.user.pk) |
            Q(clinic__owner=self.request.user)
        ).distinct()


class PatientSchedule(ListAPIView):
    """
    Agendamentos do paciente
    """
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Schedule.objects.filter(
            Q(patient=self.kwargs['pk']),
            Q(patient__clinic__owner=self.request.user) |
            Q(patient__clinic__dentists__in=[self.request.user]) |
            Q(dentist=self.request.user)
        ).distinct()

        return queryset


class PatientMessages(ListAPIView):
    """
    Mensagens enviadas/recevidas do pacientece
    """
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering = ('date', )

    def get_queryset(self):
        return Message.objects.filter(patient=self.kwargs['pk'])
