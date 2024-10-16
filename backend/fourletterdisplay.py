#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import sys
from datetime import datetime
from cleep.core import CleepRenderer
from cleep.common import CATEGORIES
from cleep.profiles.messageprofile import MessageProfile
from cleep.profiles.alarmprofile import AlarmProfile
from .fourletterphatdriver import FourLetterPHatDriver

# used for global lib import
FOUR_LETTER_PHAT = None


class Fourletterdisplay(CleepRenderer):
    """
    Fourletterdisplay application
    """

    MODULE_AUTHOR = "Cleep"
    MODULE_VERSION = "1.2.0"
    MODULE_DEPS = []
    MODULE_DESCRIPTION = "Four-letter pHAT display"
    MODULE_LONGDESCRIPTION = (
        "This application installs all needed to use Four-letter pHAT from Piromoni.<br>"
        "It allows to display informations from your device (like weather temperature, CPU usage and more) "
        "through four letters.<br>"
        "Long text (more than 4 letters) will scroll automatically and displayed dots can be "
        "configured individually.<br>"
        "Brightness is also configurable with a night mode with a night mode"
    )
    MODULE_TAGS = ["display", "pimoroni", "digits", "segments"]
    MODULE_CATEGORY = CATEGORIES.DRIVER
    MODULE_COUNTRY = None
    MODULE_URLINFO = "https://github.com/CleepDevice/cleepmod-fourletterhat"
    MODULE_URLHELP = "https://github.com/CleepDevice/cleepmod-teleinfo/wiki"
    MODULE_URLSITE = "https://shop.pimoroni.com/products/four-letter-phat"
    MODULE_URLBUGS = "https://github.com/CleepDevice/cleepmod-teleinfo/issues"

    MODULE_CONFIG_FILE = "fourletterpdisplay.conf"
    DEFAULT_CONFIG = {
        "currentbrightness": 15,
        "brightness": 15,
        "nightmode": False,
        "nightbrightness": 4,
    }

    RENDERER_PROFILES = [MessageProfile, AlarmProfile]
    RENDERER_TYPE = "display"

    def __init__(self, bootstrap, debug_enabled):
        """
        Constructor

        Params:
            bootstrap (dict): bootstrap objects
            debug_enabled: debug status
        """
        CleepRenderer.__init__(self, bootstrap, debug_enabled)

        # members
        self.driver = FourLetterPHatDriver()
        self._register_driver(self.driver)
        self.is_night_mode = False
        self.__enabled_dots = [False, False, False, False]

    def _on_start(self):
        """
        App started
        """
        try:
            self.__change_brightness(self._get_config_field("currentbrightness"))
        except Exception:
            # drop exception when hat is not configured
            pass

        # set current time asap
        now = datetime.now()
        time_str = f"{now.hour:02}{now.minute:02}"
        self.__display_time(time_str)

    def _on_stop(self):
        """
        Stop app
        """
        try:
            self.clear()
        except Exception:
            # drop exception when hat is not configured
            pass

    def on_event(self, event):
        """
        Event received

        Args:
            event (dict): MessageRequest as dict with event values::

                {
                    event (string): event name
                    params (dict): event parameters
                    device_id (string): device that emits event or None
                    sender (string): event sender
                    startup (bool): startup event flag
                }

        """
        if event["event"].endswith("time.sunrise") and self._get_config_field(
            "nightmode"
        ):
            brightness = self._get_config_field("brightness")
            self.logger.info("Disable night mode (set brightness to %s/15)", brightness)
            self.__change_brightness(brightness)
            self.is_night_mode = True

        if event["event"].endswith("time.sunset") and self._get_config_field(
            "nightmode"
        ):
            brightness = self._get_config_field("nightbrightness")
            self.logger.info(
                "Enable night mode (restore brightness to %s/15)", brightness
            )
            self.__change_brightness(brightness)
            self.is_night_mode = False

    def on_render(self, profile_name, profile_values):
        """
        Render profile

        Args:
            profile_name (str): rendered profile name
            profile_values (dict): profile values
        """
        if profile_name == "MessageProfile":
            self.__display_time(profile_values["message"])
        if profile_name == "AlarmProfile":
            if profile_values["status"] in (
                AlarmProfile.STATUS_SCHEDULED,
                AlarmProfile.STATUS_UNSCHEDULED,
            ):
                self.__display_indicator(profile_values["count"] != 0)

    def __display_time(self, time):
        """
        Display time (with dot separator)

        Args:
            time (str): time to display (HHMM)
        """
        self.display_message(time)
        self.set_dots(middle_left=True)

    def __display_indicator(self, turn_on):
        """
        Turn on/off indicator (most right LED)

        Args:
            turn_on (bool): True to turn on indicator, False otherwise
        """
        self.set_dots(most_right=turn_on)

    def __import_lib(self):
        """
        Import hat lib

        Raises:
            Exception if driver not installed or lib not installed or screen not connected
        """
        if "fourletterphat" in sys.modules:
            self.logger.debug('Module "fourletterphat" is already loaded')
        if not self.driver.is_installed():
            raise Exception("Four-letter pHAT driver is not installed")

        try:
            global FOUR_LETTER_PHAT
            FOUR_LETTER_PHAT = importlib.import_module("fourletterphat")
        except Exception as error:
            raise Exception(
                "Four-letter pHAT does not seem connected. Please check hardware"
            ) from error

    def enable_night_mode(self, enable):
        """
        Enable night mode reducing brightness when sunset event occured.

        Args:
            enable (bool): Enable night mode
        """
        self._check_parameters([{"name": "enable", "value": enable, "type": bool}])

        self._set_config_field("nightmode", enable)

        if enable and self.is_night_mode:
            self.__change_brightness(self._get_config_field("nightbrightness"))
        else:
            self.__change_brightness(self._get_config_field("brightness"))

    def set_night_mode_brightness(self, brightness):
        """
        Set nightmode brightness

        Args:
            brightness (int): brighness value (0..15)
        """
        self._check_parameters(
            [
                {
                    "name": "brightness",
                    "value": brightness,
                    "type": int,
                    "validator": lambda val: 0 <= val <= 15,
                    "message": 'Parameter "brightness" must be between 0..15',
                },
            ]
        )

        self._set_config_field("nightbrightness", brightness)

        # change brightness
        if self.is_night_mode:
            self.__change_brightness(brightness)

    def clear(self):
        """
        Clear display
        """
        self.__import_lib()
        FOUR_LETTER_PHAT.clear()
        FOUR_LETTER_PHAT.show()

    def display_message(self, message):
        """
        Display specified message (only 4 chars displayed)

        Args:
            message (string): message to display
        """
        self._check_parameters([{"name": "message", "value": message, "type": str}])

        self.__import_lib()
        FOUR_LETTER_PHAT.print_str(message)
        FOUR_LETTER_PHAT.show()

    def set_brightness(self, brightness):
        """
        Change display brightness

        Args:
            brightness (int): brighness value (0..15)
        """
        self._check_parameters(
            [
                {
                    "name": "brightness",
                    "value": brightness,
                    "type": int,
                    "validator": lambda val: 0 <= val <= 15,
                    "message": 'Parameter "brightness" must be between 0..15',
                },
            ]
        )

        # save value
        self._set_config_field("brightness", brightness)

        # change brightness
        if not self.is_night_mode:
            self.__change_brightness(brightness)

    def __change_brightness(self, brightness):
        """
        Change brightness

        Args:
            brightness (int): brighness value (0..15)
        """
        self.__import_lib()
        FOUR_LETTER_PHAT.set_brightness(brightness)

        # store current brightness to be able to restore it after restart
        self._set_config_field("currentbrightness", brightness)

    def set_dots(
        self, most_left=None, middle_left=None, middle_right=None, most_right=None
    ):
        """
        Turn on/off specified dots

        Args:
            most_left (bool, optional): True to turn on, False to turn off, None to let current state. Defaults to None.
            middle_left (bool, optional): True to turn on, False to turn off, None to let current state. Defaults to None.
            middle_right (bool, optional): True to turn on, False to turn off, None to let current state. Defaults to None.
            most_right (bool, optional): True to turn on, False to turn off, None to let current state. Defaults to None.
        """
        self.logger.debug(
            "set dots: [%s][%s][%s][%s]",
            most_left,
            middle_left,
            middle_right,
            most_right,
        )
        self.__import_lib()
        if most_left is not None:
            self.__enabled_dots[0] = most_left
        if middle_left is not None:
            self.__enabled_dots[1] = middle_left
        if middle_right is not None:
            self.__enabled_dots[2] = middle_right
        if most_right is not None:
            self.__enabled_dots[3] = most_right

        for led, value in enumerate(self.__enabled_dots):
            FOUR_LETTER_PHAT.set_decimal(led, value)

        FOUR_LETTER_PHAT.show()
