from arx.plugins.ssh import SSHPlugin
from arx.core.exceptions import ArxExecutionException
from arx.core.registry import ArxRegistry, with_plugin
from arx.core.brick import ArxBrick
from needystates import State, StateOperations, need_handler
import configparser
from needystates.need_filters import *


@ArxRegistry.brick
class SSHINIConf(ArxBrick):
    state_template = State
    plugin_class = SSHPlugin
    name = "INIConf"

    def __init__(self, path, desired_state, plugin_config):
        self.path = path
        self.address_path_append = [path]
        self.plugin_config = plugin_config
        self.desired_state = self.get_state_object(desired_state)

    def get_cstate(self):
        try:
            raw_config_file = self.plugin.send_command(f"cat {self.path}")
        except ArxExecutionException as e:
            if "No such file or directory" in e.msg:
                return self.get_state_object({})
            else:
                raise e
        else:
            c_config = configparser.ConfigParser()
            c_config.read_string(raw_config_file)
            parsed_dict = {s:dict(c_config.items()) for s in c_config.sections()}
        return self.get_state_object(parsed_dict)

    @ArxRegistry.handler(AddressPathExactFilter(['INIConf', '/etc/yum.repos.d/mariadb.repo']))
    def set_config_file_value(need, plugin):
        path = need.address_path[1]
        try:
            raw_config_file = plugin.send_command(f"cat {path}")
        except ArxExecutionException as e:
            if "No such file or directory" in e.msg:
                plugin.send_command(f"touch {path}")
                raw_config_file = ""
            else:
                raise e
        c_config = configparser.ConfigParser()
        c_config.read_string(raw_config_file)
        attr_path = []
        if need.parent_states:
            attr_path = need.parent_states
        attr_path.append(need.attribute)
        current_level = attr_path[0]
        for attr in attr_path:
            if attr != need.attribute:
                current_level[attr] = {}
                current_level = c_config[attr]
            else:
                current_level.update({need.attribute: need.value})
        output = ""
        c_config.write(output)
        print(output)





