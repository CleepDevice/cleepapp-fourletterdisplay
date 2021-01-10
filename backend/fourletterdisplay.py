#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
from cleep.core import CleepRenderer
from cleep.common import CATEGORIES
from cleep.profiles.displayMessageProfile import DisplayMessageProfile
from .fourLetterPHatDriver import FourLetterPHatDriver

# use for global lib import
FOUR_LETTER_PHAT = None

class Fourletterdisplay(CleepRenderer):
    """
    Fourletterdisplay application
    """
    MODULE_AUTHOR = 'Cleep'
    MODULE_VERSION = '1.0.0'
    MODULE_DEPS = []
    MODULE_DESCRIPTION = 'Four-letter pHAT display'
    MODULE_LONGDESCRIPTION = 'This application installs all needed to use Four-letter pHAT from Piromoni.<br>\
                             It allows to display informations from your device (like weather temperature, CPU usage and more) \
                             through four letters.<br>\
                             Long text (more than 4 letters) will scroll automatically.'
    MODULE_TAGS = ['display', 'pimoroni', 'digits', 'segments']
    MODULE_CATEGORY = CATEGORIES.DRIVER
    MODULE_COUNTRY = None
    MODULE_URLINFO = 'https://github.com/tangb/cleepmod-fourletterhat'
    MODULE_URLHELP = 'https://github.com/tangb/cleepmod-teleinfo/wiki'
    MODULE_URLSITE = 'https://shop.pimoroni.com/products/four-letter-phat'
    MODULE_URLBUGS = 'https://github.com/tangb/cleepmod-teleinfo/issues'

    MODULE_CONFIG_FILE = 'fourletterpdisplay.conf'
    DEFAULT_CONFIG = {
        'brightness': 15,
        'nightmode': False,
        'nightbrightness': 4,
    }

    RENDERER_PROFILES = [DisplayMessageProfile]
    RENDERER_TYPE = 'display'

    def __init__(self, bootstrap, debug_enabled):
        """
        Constructor

        Params:
            bootstrap (dict): bootstrap objects
            debug_enabled: debug status
        """
        CleepRenderer.__init__(self, bootstrap, debug_enabled)

        # members
        self.driver = FourLetterPHatDriver({
            'cleep_filesystem': bootstrap['cleep_filesystem'],
        })
        self._register_driver(self.driver)

    def _configure(self):
        """
        Configure module.
        """
        # set configured brightness
        try:
            self.set_brightness(self._get_config_field('brightness'))
        except Exception:
            # drop exception when hat is not configured
            pass

    def _on_stop(self):
        """
        Stop module
        """
        try:
            self.clear()
        except Exception:
            # drop exception when hat is not configured
            pass

    def on_event(self, event):
        """
        Event received

        Params:
            event (MessageRequest): event data
        """
        if event['event'].endswith('time.sunrise') and self._get_config_field('nightmode'):
            brightness = self._get_config_field('brightness')
            self.logger.info('Enable night mode (set brightness to %s/15)' % brightness)
            self.set_brightness(brightness)

        if event['event'].endswith('time.sunset') and self._get_config_field('nightmode'):
            brightness = self._get_config_field('nightbrightness')
            self.logger.info('Disable night mode (restore brightness to %s/15)' % brightness)
            self.set_brightness(brightness)

    def on_render(self, profile, params):
        """
        Render profile

        Args:
            profile (string): profile rendered
            params (dict): profile parameters
        """
        if profile == 'DisplayMessageProfile':
            self.display_message(params['message'])
            self.set_dots(middle_left=True)

    def __import_lib(self):
        """
        Import hat lib

        Raises:
            Exception if driver not installed or lib not installed or screen not connected
        """
        if not self.driver.is_installed():
            raise Exception('Four-letter pHAT driver is not installed')
        try:
            global FOUR_LETTER_PHAT
            FOUR_LETTER_PHAT = importlib.import_module('fourletterphat')
        except Exception as error:
            raise Exception('Four-letter pHAT does not seem connected. Please check hardware') from error

    def enable_night_mode(self, enable):
        """
        Enable night mode reducing brightness when sunset event occured.

        Args:
            enable (bool): Enable night mode
        """
        self._check_parameters([
            {'name': 'enable', 'value': enable, 'type': bool}
        ])

        self._set_config_field('nightmode', enable)

        if not enable:
            # restore configured brightness
            self.set_brightness(self._get_config_field('brightness'))

    def set_night_mode_brightness(self, brightness):
        """
        Set nightmode brightness

            brightness (int): brighness value (0..15)
        """
        self._check_parameters([
            {
                'name': 'brightness',
                'value': brightness,
                'type': int,
                'validator': lambda val: 0 <= val <= 15,
                'message': 'Parameter "brightness" must be between 0..15'
            },
        ])

        self._set_config_field('nightbrightness', brightness)

    def clear(self):
        """
        Clear display
        """
        self.__import_lib()
        FOUR_LETTER_PHAT.clear()
        FOUR_LETTER_PHAT.show()

    def display_message(self, message):
        """
        Display specified message

        Args:
            message (string): message to display
        """
        self._check_parameters([
            {'name': 'message', 'value': message, 'type': str}
        ])

        self.__import_lib()
        FOUR_LETTER_PHAT.scroll_print(message)

    def set_brightness(self, brightness):
        """
        Change display brightness

        Args:
            brightness (int): brighness value (0..15)
        """
        self._check_parameters([
            {
                'name': 'brightness',
                'value': brightness,
                'type': int,
                'validator': lambda val: 0 <= val <= 15,
                'message': 'Parameter "brightness" must be between 0..15',
            },
        ])

        # save value
        self._set_config_field('brightness', brightness)

        self.__import_lib()
        FOUR_LETTER_PHAT.set_brightness(brightness)

    def set_dots(self, most_left=False, middle_left=False, middle_right=False, most_right=False):
        """
        Turn on/off specified dots
        """
        self.__import_lib()
        FOUR_LETTER_PHAT.set_decimal(0, most_left)
        FOUR_LETTER_PHAT.set_decimal(1, middle_left)
        FOUR_LETTER_PHAT.set_decimal(2, middle_right)
        FOUR_LETTER_PHAT.set_decimal(3, most_right)
        FOUR_LETTER_PHAT.show()

