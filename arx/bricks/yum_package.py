from arx.plugins.ssh import SSHPlugin
from arx.core.registry import ArxRegistry
from arx.core.brick import ArxBrick
from needystates import State, StateOperations
from needystates.need_filters import *


class PackageState(State):
    attribute_descriptors = {
        'installed': {
            StateOperations.SET: 'This will install #value'
        },
        'version': {
            StateOperations.SET: 'This will upgrade the package from #old_value to #value'
        }
    }

@ArxRegistry.brick
class YumPackage(ArxBrick):
    state_template = PackageState
    plugin_class = SSHPlugin
    name = "YumPackage"

    def __init__(self, desired_state, plugin_config):
        self.plugin_config = plugin_config
        self.desired_state = self.get_state_object(desired_state)

    def get_cstate(self):
        packages_lines = self.plugin.send_command(f"yum list installed -q").split('\n')
        for line in packages_lines:
            if "Installed Packages" == line.strip():
                header_index = packages_lines.index(line)
        packages_lines_noheader = packages_lines[header_index + 1:]
        state = {}
        for line in packages_lines_noheader:
            items = line.split()
            package_name_arch = items[0].split('.')
            package_name = package_name_arch[0]
            package_arch = package_name_arch[1]
            package_version = items[1]
            state.update({package_name: {'installed': True, 'arch': package_arch, 'version': package_version}})
        for package in self.desired_state.config_keys:
            if package not in state.keys():
                state.update({package: {'installed': False}})
        return self.get_state_object(state)

