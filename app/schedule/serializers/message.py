from rest_framework.serializers import ModelSerializer

from app.schedule.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_id', 'content', 'date', 'status')
