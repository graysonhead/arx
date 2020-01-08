from arx.core.exceptions import ArxNotImplementedException
from needystates import State, StateOperations, need_handler
from functools import wraps


class ArxBrick(object):
    plugin_class = None
    plugin_config = {}
    plugin = None
    desired_state = None
    current_state = None
    name = ''
    state_template = State


    def init_plugin(self):
        self.plugin = self.plugin_class(self.plugin_config)
        self.plugin.connect()

    def get_state_metadata(self):
        return {"plugin_config": self.plugin_config,
                "desired_state": self.desired_state,
                "plugin": self.plugin_class}

    def get_address_path(self):
        addr_path = [self.name]
        if getattr(self, 'address_path_append', None) is not None:
            for li in self.address_path_append:
                addr_path.append(li)
        return addr_path

    def get_state_object(self, state_dict):
        return self.state_template(state_dict, address_path=self.get_address_path(), metadata=self.get_state_metadata())

    def get_cstate(self):
        raise ArxNotImplementedException(msg="This brick doesn't implement the 'get_cstate' method")

    def determine_needs(self):
        self.current_state = self.get_cstate()
        return self.desired_state.determine_needs(self.current_state, strict=True)






