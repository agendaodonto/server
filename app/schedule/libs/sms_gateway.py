import requests
from requests.exceptions import ConnectionError

HTTP_ERROR_CODES = [500, 501, 502, 503, 504, 505]


# noinspection PyDefaultArgument,PyShadowingBuiltins
class SMSGateway(object):
    BASE_URL = 'https://smsgateway.me'

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def make_request(self, url: str, method: str, fields: dict = {}) -> dict:
        fields['email'] = self.__username
        fields['password'] = self.__password

        url = ''.join([self.BASE_URL, url])

        result = {}
        try:
            if method == 'GET':
                req = requests.get(url, params=fields)
            elif method == 'POST':
                req = requests.post(url, data=fields)
            else:
                raise ValueError('Method {} doesn\'t exists'.format(method))
        except ConnectionError:
            return {'response': {'success': False}}

        result['status'] = req.status_code

        if req.status_code in HTTP_ERROR_CODES:
            result['response'] = {'success': False}
        else:
            result['response'] = req.json()

        return result

    def get_devices(self, page=1):
        return self.make_request('/api/v3/devices', 'GET', {'page': page})

    def get_device(self, id):
        url = ''.join(['/api/v3/devices/view/', str(id)])
        return self.make_request(url, 'GET')

    def get_contacts(self, page=1):
        return self.make_request('/api/v3/contacts', 'GET', {'page': page})

    def get_contact(self, id):
        url = ''.join(['/api/v3/contacts/view/', str(id)])
        return self.make_request(url, 'GET')

    def get_messages(self, page=1):
        return self.make_request('/api/v3/messages', 'GET', {'page': page})

    def get_message(self, id):
        url = ''.join(['/api/v3/messages/view/', str(id)])
        return self.make_request(url, 'GET')

    def create_contact(self, name, number):
        return self.make_request('/api/v3/contacts/create', 'POST', {'name': name, 'number': number})

    def send_message_to_number(self, to, message, device, options={}):
        options.update({'number': to,
                        'message': message,
                        'device': device})
        return self.make_request('/api/v3/messages/send', 'POST', options)

    def send_message_to_many_numbers(self, to, message, device, options={}):
        options.update({'number': to,
                        'message': message,
                        'device': device})
        return self.make_request('/api/v3/messages/send', 'POST', options)

    def send_message_to_contact(self, to, message, device, options={}):
        options.update({'contact': to,
                        "message": message,
                        'device': device})
        return self.make_request('/api/v3/messages/send', 'POST', options)

    def send_message_to_many_contact(self, to, message, device, options={}):
        options.update({'contact': to,
                        "message": message,
                        'device': device})
        return self.make_request('/api/v3/messages/send', 'POST', options)
