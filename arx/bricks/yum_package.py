from arx.plugins.ssh import SSHPlugin
from arx.core.registry import ArxRegistry
from arx.core.brick import ArxBrick
from needystates import State, StateOperations, Need
from needystates.operations import Operations
from needystates.need_filters import *


class PackageOperations(Operations):
    INSTALL = 1
    UPGRADE = 2
    UNINSTALL = 3

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
            state.update({package_name: {'installed': True, 'arch': package_arch}})
            if len(items) > 1:
                package_version = items[1]
                state[package_name].update({'version': package_version})
        return self.get_state_object(state)

    def determine_needs(self, strict=None):
        needs = []
        self.current_state = self.get_cstate()
        packages_requested = self.desired_state.render_dict()
        packages_installed = self.current_state.render_dict()
        for package, values in packages_requested.items():
            if package not in packages_installed and values['installed']:
                install_version = None
                if values.get('version', None):
                    install_version = values['version']
                needs.append(Need(package,
                                  PackageOperations.INSTALL,
                                  metadata=self.get_state_metadata(),
                                  address_path=self.get_address_path(),
                                  value=install_version))
        return needs

    @ArxRegistry.handler(OperationFilter(PackageOperations.INSTALL))
    def install_package(need, plugin):
        version_string = ''
        if need.value:
            version_string = f"-{need.value}"
        return plugin.send_command(f"yum install {need.attribute}{version_string} -y")

