from .track_repository import TrackRepository
from .current_track_notifier import CurrentTrackNotifier


class ServiceNotRegisteredError(Exception):
    pass


class ServiceRegistry:

    def __init__(self):
        self._services = {}

    def register(self, name, cls):
        self._services[name] = {
            "factory": cls,
            "instance": None,
        }

    def get(self, name):
        if name not in self._services:
            raise ServiceNotRegisteredError()

        service_entry = self._services[name]

        if not service_entry["instance"]:
            service_entry["instance"] = service_entry["factory"]()

        return service_entry["instance"]


service_registry = ServiceRegistry()


def register_services():
    service_registry.register("track_repository", TrackRepository)
    service_registry.register("current_track_notifier", CurrentTrackNotifier)

register_services()
