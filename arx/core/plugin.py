from arx.core.exceptions import ArxValidationError
from arx.core.registry import PLUGIN_INSTANCES


class ArxPluginBase(object):

    attributes = {}

    def __init__(self, config: dict):
        self.config = config
        self.validate(config)
        self.load_config(config)
        PLUGIN_INSTANCES.append(self)

    def validate(self, config):
        for key, value in config.items():
            if key not in self.attributes.keys():
                raise ArxValidationError(f"Key {key} not an allowed attribute for {self},"
                                         f"Allowed attributes are {self.attributes.keys()}")
            if not isinstance(value, self.attributes[key]['type']):
                raise ArxValidationError(f"Key {key}'s value must be {self.attributes[key]['type']} "
                                         f"but it is {type(value)}")
            if type(value) is list or type(value) is tuple:
                if self.attributes[key].get('length', None) is not None:
                    if len(value) != self.attributes[key]['length']:
                        raise ArxValidationError(f"{key}'s length must be {self.attributes[key]['length']} but "
                                                 f"it is instead {len(value)}")
        for key, value in self.attributes.items():
            if value.get('required', None) is True:
                if key not in config:
                    raise ArxValidationError(f"{key} is a required argument for {self}")

    def load_config(self, config):
        for key, value in config.items():
            setattr(self, key, value)
