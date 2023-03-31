from typing import Callable


class Event:
    def __init__(self):
        self._callbacks: dict[str, list[Callable]] = {}

    def add_listener(self, event: str, callback: Callable):
        if event not in self._callbacks: self._callbacks[event] = []
        self._callbacks[event].append(callback)

    def remove_listener(self, event: str, callback: Callable):
        self._callbacks.get(event, []).remove(callback)

    def trigger_listener(self, event: str, *args, **kwargs):
        for callback in self._callbacks[event]:
            callback(self, *args, **kwargs)
