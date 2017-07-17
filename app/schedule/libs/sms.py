import datetime
import logging
import time

from .sms_gateway import SMSGateway


class SMS:
    SMS_TIMEOUT = 60 * 15  # Segundos
    MIN_BATTERY = 15
    MIN_SIGNAL = 10
    MIN_TIME = 60 * 60 * 10

    def __init__(self, email: str, password: str):
        self.sms_gateway = SMSGateway(email, password)
        self.device = self.get_best_device()

    def get_best_device(self) -> str:
        """
        Returns the ID of the best device available
        :return:
        """
        logger = logging.getLogger(__name__)
        response = self.sms_gateway.get_devices()['response']
        best_device = None
        if response['success']:
            devices = response['result']['data']
            for device in devices:
                try:
                    self.check_device_suitability(device)
                    if not best_device:
                        best_device = device
                    elif int(device['last_seen']) > int(best_device['last_seen']):
                        best_device = device
                except NotSuitableDevice as e:
                    logger.warning("Device {} not suitable because {}".format(device['id'], e))

        if not best_device:
            raise DeviceNotFoundError('No Device found.')
        logger.info("""
                    Best device found: {} - {}
                    Signal: {}
                    Battery: {}%
                    Connection: {}
                    """.format(best_device['id'], best_device['model'], best_device['signal'], best_device['battery'],
                               best_device['connection_type']))

        return best_device['id']

    def check_device_suitability(self, device):
        if device['provider'] == '':
            raise NotSuitableDevice('Device not attached to the network')
        if int(device['signal']) < self.MIN_SIGNAL:
            raise NotSuitableDevice('Low Signal ({})'.format(device['signal']))
        if int(device['battery']) < self.MIN_BATTERY:
            raise NotSuitableDevice('Low battery ({})'.format(device['battery']))
        if int(time.time()) - int(device['last_seen']) > self.MIN_TIME:
            raise NotSuitableDevice('Missing for more than {} minutes'.format(self.MIN_TIME))

    def send_message(self, to: str, message: str) -> bool:
        message = self.sms_gateway.send_message_to_number(to, message, self.device)['response']
        if message['success']:
            return self.wait_message_sent(message['result']['success'][0]['id'])
        else:
            return False

    def wait_message_sent(self, message_id: str):
        start_time = datetime.datetime.now()
        while True:
            message = self.sms_gateway.get_message(message_id)['response']
            if message['result']['status'] == 'sent':
                return True
            elif message['result']['status'] == 'failed':
                logging.warning('Failure while sending SMS: {}'.format(message['result']['error']))
                return False
            elif (datetime.datetime.now() - start_time).seconds >= self.SMS_TIMEOUT:
                logging.warning('Timeout while sending SMS')
                return False

            time.sleep(1)


class DeviceNotFoundError(Exception):
    pass


class NotSuitableDevice(Exception):
    pass


class DummySMS:
    def __init__(self, user, password):
        pass

    def send_message(self, to, message):
        return True
