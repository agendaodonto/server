from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from app.schedule.models import DentalPlan
from app.schedule.serializers.dental_plan import DentalPlanSerializer


class DentalPlanFilter(FilterSet):
    name = CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = DentalPlan
        fields = ['name']


class DentalPlanList(ListCreateAPIView):
    """
    Lista de planos
    """
    serializer_class = DentalPlanSerializer
    queryset = DentalPlan.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_class = DentalPlanFilter


class DentalPlanDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhe do plano
    """
    serializer_class = DentalPlanSerializer
    queryset = DentalPlan.objects.all()
    permission_classes = (IsAuthenticated,)
