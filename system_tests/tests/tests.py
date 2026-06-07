import unittest

from utils.channel_access import ChannelAccess  # pyright: ignore
from utils.ioc_launcher import get_default_ioc_dir  # pyright: ignore
from utils.test_modes import TestModes  # pyright: ignore
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim  # pyright: ignore

DEVICE_PREFIX = "QNW_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("QNW"),
        "emulator": "quantumnorthwest",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class QuantumNorthwestTests(unittest.TestCase):
    """
    Tests for the QNW IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("quantumnorthwest", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    @skip_if_recsim("requires lewis")
    def test_id(self):
        self.ca.assert_that_pv_is("ID", "t2", timeout=20)

    @skip_if_recsim("requires lewis")
    def test_max_speed(self):
        self._lewis.backdoor_set_on_device("max_stirrer_speed", 1234)
        self.ca.assert_that_pv_is_number("STIR:SPEED:MAX", 1234, tolerance=0.01, timeout=20)

    @skip_if_recsim("requires lewis")
    def test_min_speed(self):
        self._lewis.backdoor_set_on_device("min_stirrer_speed", 12)
        self.ca.assert_that_pv_is_number("STIR:SPEED:MIN", 12, tolerance=0.01, timeout=20)

    def test_speed(self):
        self.ca.assert_setting_setpoint_sets_readback(999, "STIR:SPEED")
        self.ca.assert_setting_setpoint_sets_readback(0, "STIR:SPEED")
        self.ca.assert_setting_setpoint_sets_readback(995, "STIR:SPEED")

    def test_temperature_control_enabled(self):
        self.ca.assert_setting_setpoint_sets_readback("No", "TEMP:ENABLED")
        self.ca.assert_setting_setpoint_sets_readback("Yes", "TEMP:ENABLED")

    def test_temperature(self):
        self.ca.set_pv_value("TEMP:SP", 56.78)
        self.ca.assert_that_pv_is_number("TEMP:SP:RBV", 56.78, tolerance=0.01)
        self.ca.assert_that_pv_is_number("TEMP", 56.78, tolerance=0.01)

        self.ca.set_pv_value("TEMP:SP", -12.34)
        self.ca.assert_that_pv_is_number("TEMP:SP:RBV", -12.34, tolerance=0.01)
        self.ca.assert_that_pv_is_number("TEMP", -12.34, tolerance=0.01)

    @skip_if_recsim("requires lewis")
    def test_temperature_status(self):
        self._lewis.backdoor_set_on_device("temperature_status", "S")
        self.ca.assert_that_pv_is("TEMP:STAT", "Stable")

        self._lewis.backdoor_set_on_device("temperature_status", "C")
        self.ca.assert_that_pv_is("TEMP:STAT", "Changing")

    @skip_if_recsim("requires lewis")
    def test_min_temperature(self):
        self._lewis.backdoor_set_on_device("min_temperature", -25)
        self.ca.assert_that_pv_is_number("TEMP:MIN", -25, tolerance=0.01, timeout=20)

    @skip_if_recsim("requires lewis")
    def test_max_temperature(self):
        self._lewis.backdoor_set_on_device("max_temperature", 175)
        self.ca.assert_that_pv_is_number("TEMP:MAX", 175, tolerance=0.01, timeout=20)

    @skip_if_recsim("requires lewis")
    def test_probe_temperature(self):
        self._lewis.backdoor_set_on_device("probe_temperature", 12.34)
        self.ca.assert_that_pv_is_number("TEMP:PROBE", 12.34, tolerance=0.01, timeout=20)

    @skip_if_recsim("requires lewis")
    def test_heat_exchanger_temperature(self):
        self._lewis.backdoor_set_on_device("heat_exchanger_temperature", 12.34)
        self.ca.assert_that_pv_is_number("TEMP:HX", 12.34, tolerance=0.01, timeout=20)

        self._lewis.backdoor_set_on_device("heat_exchanger_temperature", 56.78)
        self.ca.assert_that_pv_is_number("TEMP:HX", 56.78, tolerance=0.01, timeout=20)

    def test_temp_ramp_rate(self):
        self.ca.set_pv_value("TEMP:RATE:SP", 0.34)
        self.ca.assert_that_pv_is_number("TEMP:RATE", 0.34, tolerance=0.01, timeout=20)

        self.ca.set_pv_value("TEMP:RATE:SP", 0.56)
        self.ca.assert_that_pv_is_number("TEMP:RATE", 0.56, tolerance=0.01, timeout=20)
