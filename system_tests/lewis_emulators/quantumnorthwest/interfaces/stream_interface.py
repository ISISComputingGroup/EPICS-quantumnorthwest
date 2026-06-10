import logging
import typing

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if typing.TYPE_CHECKING:
    from ..device import SimulatedQuantumNorthwest

if_connected = conditional_reply("connected")


@has_log
class QuantumNorthwestStreamInterface(StreamInterface):
    in_terminator = "]"
    out_terminator = "]"

    def __init__(self) -> None:
        super(QuantumNorthwestStreamInterface, self).__init__()
        self.log: logging.Logger
        self.device: SimulatedQuantumNorthwest

        self.commands = {
            CmdBuilder(self.get_id).escape("[F1 ID ?").eos().build(),
            CmdBuilder(self.get_max_stirrer_speed).escape("[F1 MS ?").eos().build(),
            CmdBuilder(self.get_min_stirrer_speed).escape("[F1 LS ?").eos().build(),
            CmdBuilder(self.get_speed).escape("[F1 SS ?").eos().build(),
            CmdBuilder(self.set_speed).escape("[F1 SS S ").int().eos().build(),
            CmdBuilder(self.get_status).escape("[F1 IS ?").eos().build(),
            CmdBuilder(self.set_temp_enabled).escape("[F1 TC ").enum("+", "-").eos().build(),
            CmdBuilder(self.get_temp).escape("[F1 CT ?").eos().build(),
            CmdBuilder(self.set_temp).escape("[F1 TT S ").float().eos().build(),
            CmdBuilder(self.get_temp_sp).escape("[F1 TT ?").eos().build(),
            CmdBuilder(self.get_max_temp).escape("[F1 MT ?").eos().build(),
            CmdBuilder(self.get_min_temp).escape("[F1 LT ?").eos().build(),
            CmdBuilder(self.get_probe_temp).escape("[F1 PT ?").eos().build(),
            CmdBuilder(self.get_temp_rate).escape("[F1 RR ?").eos().build(),
            CmdBuilder(self.set_temp_rate).escape("[F1 RR S ").float().eos().build(),
            CmdBuilder(self.get_hx_temp).escape("[F1 HT ?").eos().build(),
            CmdBuilder(self.disable_auto_reporting).escape("[F1 XX R-").eos().build(),
        }

    def handle_error(self, request: str, error: str) -> None:
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def disable_auto_reporting(self) -> None:
        pass

    @if_connected
    def get_id(self) -> str:
        return f"[F1 ID {self.device.id}"

    @if_connected
    def get_max_stirrer_speed(self) -> str:
        return f"[F1 MS {self.device.max_stirrer_speed}"

    @if_connected
    def get_min_stirrer_speed(self) -> str:
        return f"[F1 LS {self.device.min_stirrer_speed}"

    @if_connected
    def get_speed(self) -> str:
        return f"[F1 SS {self.device.stirrer_speed}"

    @if_connected
    def set_speed(self, speed: str) -> None:
        self.device.stirrer_speed = int(speed)

    @if_connected
    def get_status(self) -> str:
        stirrer = "+" if self.device.stirrer_speed > 0 else "-"
        tc = "+" if self.device.temp_enabled else "-"
        temp_status = str(self.device.temperature_status)
        return f"[F1 IS 0{stirrer}{tc}{temp_status}"

    @if_connected
    def set_temp_enabled(self, enabled: str) -> None:
        self.device.temp_enabled = enabled == "+"

    @if_connected
    def get_temp(self) -> str:
        return f"[F1 CT {self.device.temperature}"

    @if_connected
    def set_temp(self, temperature: float) -> None:
        self.device.temperature = temperature

    @if_connected
    def get_temp_sp(self) -> str:
        return f"[F1 TT {self.device.temperature}"

    @if_connected
    def get_min_temp(self) -> str:
        return f"[F1 LT {self.device.min_temperature}"

    @if_connected
    def get_max_temp(self) -> str:
        return f"[F1 MT {self.device.max_temperature}"

    @if_connected
    def get_probe_temp(self) -> str:
        return f"[F1 PT {self.device.probe_temperature}"

    @if_connected
    def get_temp_rate(self) -> str:
        return f"[F1 RR {self.device.temperature_rate}"

    @if_connected
    def set_temp_rate(self, rate: float) -> None:
        self.device.temperature_rate = rate

    @if_connected
    def get_hx_temp(self) -> str:
        return f"[F1 HT {self.device.heat_exchanger_temperature}"
