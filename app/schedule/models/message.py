from django.db.models import CharField, DateTimeField
from django.db.models.fields.related import ForeignKey
from model_utils.models import TimeStampedModel

from app.schedule.models import Patient


class Message(TimeStampedModel):

    message_id = CharField('Identificador Único', max_length=30, unique=True, null=False)
    content = CharField('Conteúdo', max_length=300)
    date = DateTimeField('Data da mensagem', null=True)
    status = CharField('Status', max_length=15)
    patient = ForeignKey(Patient)
