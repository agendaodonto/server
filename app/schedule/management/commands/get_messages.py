import logging
from datetime import datetime

import pytz
from django.core.management import BaseCommand
from django.conf import settings

from app.schedule.libs.sms_gateway import SMSGateway
from app.schedule.models import Patient, Message


class Command(BaseCommand):
    tz = pytz.timezone(settings.TIME_ZONE)

    def handle_date(self, date):
        if date != 0:
            return datetime.fromtimestamp(date, self.tz)
        else:
            return None

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        username = settings.SMS_GATEWAY_USER
        password = settings.SMS_GATEWAY_PASSWORD
        gateway = SMSGateway(username, password)
        response = gateway.get_messages()

        if not response['response']['success']:
            logger.warning('Failed to fetch the messages')
            return

        messages = response['response']['result']

        for message in messages:
            last_digits = message['contact']['number'][-11:]
            if not Message.objects.filter(message_id=message['id']).exists():
                try:
                    patient = Patient.objects.get(phone__endswith=last_digits)
                    received_at = self.handle_date(message['received_at'])
                    sent_at = self.handle_date(message['sent_at'])
                    message_date = sent_at if sent_at else received_at

                    Message.objects.create(
                        message_id=message['id'],
                        content=message['message'],
                        status=message['status'],
                        date=message_date,
                        patient=patient
                    )
                except Patient.DoesNotExist:
                    pass
