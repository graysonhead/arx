from arx.plugins.ssh import SSHPlugin
from arx.core.registry import ArxRegistry
from arx.core.brick import ArxBrick
from needystates import State, StateOperations, need_handler
from needystates.need_filters import *


class HostNameState(State):
    attribute_descriptors = {
        'hostname': {
            StateOperations.SET: 'This will change the hostname of the system from #old_value to #value'
        }
    }


@ArxRegistry.brick
class HostName(ArxBrick):
    state_template = HostNameState
    plugin_class = SSHPlugin
    name = 'HostName'

    def __init__(self, desired_state, plugin_config):
        self.plugin_config = plugin_config
        self.desired_state = self.get_state_object(desired_state)

    def get_cstate(self):
        hostname = self.plugin.send_command('hostname')
        return self.get_state_object({"hostname": hostname})

    @ArxRegistry.handler(AttributeFilter('hostname'), AddressPathExactFilter(['HostName']), OperationFilter(StateOperations.SET))
    def set_host_name(need, plugin):
        plugin.send_command(f'hostnamectl set-hostname {need.value}')
