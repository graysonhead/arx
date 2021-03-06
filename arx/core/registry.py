from functools import wraps
from needystates.exceptions import NeedyStatesNoMatch


REGISTERED_BRICKS = []
REGISTERED_HANDLERS = []

PLUGIN_INSTANCES = []


class ArxRegistry:

    @staticmethod
    def brick(cls):
        REGISTERED_BRICKS.append(cls)
        return cls

    @staticmethod
    def handler(*filter_args):
        # Hope you ate your wheaties today, this one is fun
        def wrapper(func):
            # Register the handler pre-wrapped with its filter functions
            REGISTERED_HANDLERS.append(check_filters(*filter_args, func=with_plugin(func)))
        return wrapper

    @staticmethod
    def get_handlers():
        return REGISTERED_HANDLERS

    @staticmethod
    def find_existing_plugin_instance(config):
        for plugin_instances in PLUGIN_INSTANCES:
            if plugin_instances.config == config:
                return plugin_instances


def check_filters(*filter_args, func=None):
    @wraps(func)
    def inner(need):
        if all([i.check_filter(need) for i in filter_args]):
            # If all provided filters return true, run the handler
            return func(need)
        else:
            # Else, raise a special Exception to let the processor know the handler wasn't a match
            raise NeedyStatesNoMatch
    return inner


def with_plugin(func):
    # This finds an existing plugin instance with a suitable configuration from the registry, else it creates a new one
    @wraps(func)
    def inner(need):
        found_instance = ArxRegistry.find_existing_plugin_instance(need.metadata['plugin_config'])
        found_instance.connect()
        if found_instance:
            return func(need, found_instance)
        else:
            plugin_class = need.metadata['plugin']
            plugin = plugin_class(need.metadata['plugin_config'])
            plugin.connect()
            return func(need, plugin)
    return inner


