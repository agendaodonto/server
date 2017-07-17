import requests


# noinspection PyDefaultArgument,PyShadowingBuiltins
class SMSGateway(object):
    BASE_URL = 'https://smsgateway.me'

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def make_request(self, url: str, method: str, fields: dict={})-> dict:
        fields['email'] = self.__username
        fields['password'] = self.__password

        url = ''.join([self.BASE_URL, url])

        if method == 'GET':
            result = {}
            r = requests.get(url, params=fields)
            result['status'] = r.status_code
            result['response'] = r.json()

            return result

        elif method == 'POST':
            result = {}
            r = requests.post(url, data=fields)
            result['status'] = r.status_code
            result['response'] = r.json()

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
