import abc


class Attributes:

    _validators = {}

    @abc.abstractmethod
    def __init__(self, **kwargs):
        self._attributes = {}
        for key, value in kwargs.items():
            if key not in self._valid_attributes:
                raise ValueError(key)
            if key in self._validator_overrides:
                value = self._validator_overrides[key](value)
            elif key in self._validators:
                value = self._validators[key](value)
            self._attributes[key] = value
