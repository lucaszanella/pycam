from onvif import ONVIFCamera
from zeep import Client

class CustomTransport(Transport):
    def __init__(self, proxies):
        Transport.__init__(self)
        self.proxies = proxies

def get(self, address, params, headers):
        """Proxy to requests.get()
        :param address: The URL for the request
        :param params: The query parameters
        :param headers: a dictionary with the HTTP headers.
        """
        response = self.session.get(
            address,
            params=params,
            headers=headers,
            timeout=self.operation_timeout,
            proxies=self.proxies)
        return response

    def post(self, address, message, headers):
        """Proxy to requests.posts()
        :param address: The URL for the request
        :param message: The content for the body
        :param headers: a dictionary with the HTTP headers.
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            log_message = message
            if isinstance(log_message, bytes):
                log_message = log_message.decode('utf-8')
            self.logger.debug("HTTP Post to %s:\n%s", address, log_message)

        response = self.session.post(
            address,
            data=message,
            headers=headers,
            timeout=self.operation_timeout,
            proxies=self.proxies)

        if self.logger.isEnabledFor(logging.DEBUG):
            media_type = get_media_type(
                response.headers.get('Content-Type', 'text/xml'))

            if media_type == 'multipart/related':
                log_message = response.content
            else:
                log_message = response.content
                if isinstance(log_message, bytes):
                    log_message = log_message.decode('utf-8')

            self.logger.debug(
                "HTTP Response from %s (status: %d):\n%s",
                address, response.status_code, log_message)

        return response

user = ''
password = ''
host = ''
port = 1234

proxies = {
    'http': 'socks5://' + user + ':' + password + '@' + host + ':' + port,
    'https': 'socks5://' + user + ':' + password + '@' + host + ':' + port
}

SocksTransport = CustomTransport(proxies)
mycam = ONVIFCamera('192.168.0.2', 80, 'user', 'passwd', '', transport=SocksTransport)