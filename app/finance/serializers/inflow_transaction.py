from rest_framework.serializers import ModelSerializer

from app.finance.models import InflowTransaction


class InflowTransactionSerializer(ModelSerializer):
    class Meta:
        model = InflowTransaction
        fields = ('amount', 'payment_holder', 'service_beneficiary', 'description', 'date', 'type')
