from collections import OrderedDict
from enum import StrEnum

from lewis.devices import StateMachineDevice

from .states import DefaultState


class ID(StrEnum):
    SPECIALITY = "00"
    T2 = "14"
    T2X2 = "24"
    TURRET6 = "34"


class TemperatureStatus(StrEnum):
    STABLE = "S"
    CHANGING = "C"


class SimulatedQuantumNorthwest(StateMachineDevice):
    def _initialize_data(self) -> None:
        """
        Initialize all of the device's attributes.
        """
        self.connected = True

        self.id = ID.T2

        self.max_stirrer_speed = 2500
        self.min_stirrer_speed = 300
        self.stirrer_speed = 1000

        self.temp_enabled = True
        self.temperature = 1.0
        self._temperature_status = TemperatureStatus.STABLE
        self.min_temperature = -40
        self.max_temperature = 110
        self.probe_temperature = 45
        self.temperature_rate = 0.12
        self.heat_exchanger_temperature = 43.21

    @property
    def temperature_status(self) -> TemperatureStatus:
        return self._temperature_status

    @temperature_status.setter
    def temperature_status(self, value: TemperatureStatus | str) -> None:
        if isinstance(value, TemperatureStatus):
            self._temperature_status = value
        else:
            self._temperature_status = TemperatureStatus(value)

    def _get_state_handlers(self) -> dict:
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self) -> str:
        return "default"

    def _get_transition_handlers(self) -> OrderedDict:
        return OrderedDict([])
