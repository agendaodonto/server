from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from app.finance.models import TransactionType
from app.finance.serializers import TransactionTypeSerializer


class TransactionTypeList(ListCreateAPIView):
    """
    Lista de Tipos de Transação
    """
    serializer_class = TransactionTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TransactionType.objects.filter(clinic__owner=self.request.user)


class TransactionTypeDetail(RetrieveUpdateDestroyAPIView):
    """
    Recupera/Apaga/Altera Tipos de Transação
    """
    serializer_class = TransactionTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TransactionType.objects.filter(clinic__owner=self.request.user)
