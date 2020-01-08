from pylxd import Client
from arx.core.exceptions import ArxConnectionError, ArxValidationError
from arx.core.plugin import ArxPluginBase

import logging
logger = logging.getLogger(__name__)


class LXDPlugin(ArxPluginBase):
    attributes = {
        'endpoint': {
            'type': str,
            'required': True
        },
        'cert': {
            'type': tuple,
            'length': 2,
            'required': True
        },
        'verify': {
            'type': bool,
            'default': True
        },
        'trust_password': {
            'type': str,
            'required': True
        }
    }
    client = None

    def connect(self):
        self.client = Client(
            endpoint=self.endpoint,
            cert=self.cert,
            verify=self.verify
        )
        if self.client.trusted is False:
            try:
                self.client.authenticate(self.trust_password)
            except Exception as e:
                raise ArxConnectionError(msg=f"LXD connection failure: {e}")

    def get_container(self, name):
        return self.client.containers.get(name)