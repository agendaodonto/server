import datetime
import logging
import time

from django.conf import settings
from smsgateway import SMSGateway, Message

from app.schedule.utils.utils import parse_js_date


class SMS:
    def __init__(self, token: str):
        self.client = SMSGateway(token)
        self.device = None

    def get_best_device(self) -> int:
        logger = logging.getLogger(__name__)
        best_device = None
        devices = self.client.search_devices()['results']

        for device in devices:
            try:
                self.check_device_suitability(device)
                if not best_device:
                    best_device = device
                else:
                    best_last_seen = parse_js_date(best_device['attributes']['last_seen'])
                    current_last_seen = parse_js_date(device['attributes']['last_seen'])
                    if best_last_seen > current_last_seen:
                        best_device = device
            except NotSuitableDevice as e:
                logger.warning("Device {} not suitable because {}".format(device['id'], e))
        else:
            logger.error('No device found')

        if not best_device:
            raise DeviceNotFoundError('No Device found.')
        logger.info("""
                    Best device found: {}
                    """.format(best_device['id']))
        self.device = best_device['id']
        return self.device

    def check_device_suitability(self, device):
        last_seen = parse_js_date(device['attributes']['last_seen'])
        if int(time.time()) - last_seen.timestamp() > settings.SMS_MIN_MISSING_TIME:
            raise NotSuitableDevice('Missing for more than {} minutes'.format(settings.SMS_MIN_MISSING_TIME))

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

    def get_best_device(self):
        return True
