from paramiko import SSHClient, RejectPolicy
from arx.core.exceptions import ArxNotConnectedError, ArxConnectionError, ArxExecutionException
from arx.core.plugin import ArxPluginBase

import logging
logger = logging.getLogger(__name__)


class SSHPlugin(ArxPluginBase):
    client = None
    attributes = {
        'hostname': {
            'type': str,
            'required': True
        },
        'username': {
            'type': str,
            'required': True
        },
        'password': {
            'type': str,
            'required': False
        },
        'port': {
            'type': int,
            'required': False
        }
    }

    def connect(self):
        """
        Adds paramiko ssh client to self.client
        :return:
        """
        if not isinstance(self.client, SSHClient):
            self.client = SSHClient()
        if getattr(self, 'port', None) is None:
            self.port = 22
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(RejectPolicy)
        self.client.connect(hostname=self.hostname,
                            port=self.port,
                            username=self.username,
                            password=self.password)

    def disconnect(self):
        if self.client:
            self.client.close()

    def send_command(self, command):
        logger.debug(f"Provider {self} sent command: {command}")
        if self.client is None:
            raise ArxNotConnectedError("You must activate the client with self.connect() before executing commands")
        stdin, stdout, stderr = self.client.exec_command(command)
        err = '\n'.join(stderr.readlines())
        if err:
            raise ArxExecutionException(msg=err)
        response = stdout.read().decode('utf-8').strip()
        logger.debug(f"Provider {self} received response: {response}")
        return response
