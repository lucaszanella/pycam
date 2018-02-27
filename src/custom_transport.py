from zeep import Transport
import requests
import sys
import logging
#sys.path.insert(0, '/home/deps/python-onvif-zeep/onvif')
#from client import * 

class CustomTransport(Transport):
    def __init__(self, timeout=None, proxies=None):
        Transport.__init__(self, timeout)
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
