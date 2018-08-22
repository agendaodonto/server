import datetime
import logging
import time

from django.conf import settings
from smsgateway import SMSGateway, Message


class SMS:
    def __init__(self, token: str):
        self.client = SMSGateway(token)
        self.device = None

    def get_latest_device(self) -> int:
        device_filter = {
            'order_by': [{'field': 'id', 'direction': 'desc'}],
            'limit': 1
        }
        devices = self.client.search_devices(device_filter)['results']

        if len(devices) <= 0:
            raise DeviceNotFoundError()

        self.device = devices[0]['id']
        return self.device

    def send_message(self, to: str, message: str) -> bool:
        message = Message(to, message, self.device)
        response = self.client.send_sms(message)
        return self.wait_message_sent(response[0]['id'])

    def wait_message_sent(self, message_id: int):
        start_time = datetime.datetime.now()
        while True:
            message = self.client.get_sms(message_id)
            if message['status'] == 'sent':
                return True
            elif message['status'] == 'failed':
                logging.warning('Failure while sending SMS')
                return False

            if (datetime.datetime.now() - start_time).seconds >= settings.SMS_TIMEOUT:
                logging.warning('Timeout while sending SMS')
                return False

            time.sleep(1)


class DeviceNotFoundError(Exception):
    pass


class NotSuitableDevice(Exception):
    pass


class DummySMS:
    def __init__(self, token):
        pass

    def send_message(self, to, message):
        return True

    def get_latest_device(self):
        return 1
