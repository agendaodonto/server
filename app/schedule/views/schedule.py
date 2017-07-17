import django_filters
import datetime
from django.db.models import Q
from django_filters.rest_framework import FilterSet
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.schedule.models import Dentist
from app.schedule.models import Schedule
from app.schedule.serializers import ScheduleListSerializer, ScheduleSerializer


class ScheduleFilter(FilterSet):
    date = django_filters.DateFromToRangeFilter(name='date')

    class Meta:
        model = Schedule
        fields = ['date', 'status', 'dentist']


class ScheduleList(ListCreateAPIView):
    """
    Lista de agendametos
    """
    queryset = Schedule.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = ScheduleFilter
    ordering = 'date'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScheduleListSerializer
        else:
            return ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(
            Q(patient__clinic__owner=self.request.user) |
            Q(patient__clinic__dentists__in=[self.request.user]) |
            Q(dentist=self.request.user)
        ).distinct()


class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes do agendamento
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Schedule.objects.filter(
            Q(patient__clinic__owner=self.request.user) |
            Q(patient__clinic__dentists__in=[self.request.user]) |
            Q(dentist=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScheduleListSerializer
        else:
            return ScheduleSerializer

class ScheduleAttendance(APIView):
    @staticmethod
    def get_data(user: Dentist, year: int):
        data = {'absences': [], 'attendances': [], 'cancellations': []}
        for month in range(1, 13):
            schedules = Schedule.objects.filter(dentist=user).filter(date__year=year).filter(date__month=month)
            data['attendances'].append(schedules.filter(status=1).count())
            data['absences'].append(schedules.filter(status=2).count())
            data['cancellations'].append(schedules.filter(status=3).count())

        return data

    def get(self, request):
        year = request.query_params.get('year', datetime.datetime.now().year)
        return Response(self.get_data(request.user, year))
