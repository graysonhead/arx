from arx.plugins.ssh import SSHPlugin
from arx.core.exceptions import ArxExecutionException
from arx.core.registry import ArxRegistry, with_plugin
from arx.core.brick import ArxBrick
from needystates import State, StateOperations, need_handler
import configparser
from needystates.need_filters import *
import os
from tempfile import NamedTemporaryFile

@ArxRegistry.brick
class SSHINIConf(ArxBrick):
    state_template = State
    plugin_class = SSHPlugin
    name = "INIConf"
    default_strict = True

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
            parsed_dict = {s: dict(c_config.items(s)) for s in c_config.sections()}
        return self.get_state_object(parsed_dict)

    @ArxRegistry.handler(AddressPathContainsFilter('INIConf'))
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
        if need.parent_states[0] not in c_config.sections():
            c_config.add_section(need.parent_states[0])
        c_config.set(need.parent_states[0], need.attribute, need.value)
        f = NamedTemporaryFile(mode='w+', delete=False)
        with open(f.name, 'w+') as new:
            c_config.write(new)
        with open(f.name, 'r') as new:
            text = new.read()
            plugin.send_command(f"echo \"{text}\" > {need.address_path[1]}")
        os.unlink(f.name)

