#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleep.libs.drivers.driver import Driver
from cleep.libs.configs.configtxt import ConfigTxt
from cleep.libs.configs.etcmodules import EtcModules

class FourLetterPHatDriver(Driver):
    """
    Pimoroni Four-letter pHat driver for Cleep
    """

    DRIVER_NAME = 'Pimoroni Four-letter pHat'
    MODULE_I2C_DEV = 'i2c-dev'

    def __init__(self):
        """
        Constructor
        """
        Driver.__init__(self, Driver.DRIVER_DISPLAY, FourLetterPHatDriver.DRIVER_NAME)

    def _on_registered(self):
        """
        Driver is registered
        """
        # members
        self.config_txt = ConfigTxt(self.cleep_filesystem)
        self.etc_modules = EtcModules(self.cleep_filesystem)

    def _install(self, params):
        """
        Install driver
        """
        self.config_txt.enable_i2c()
        self.etc_modules.enable_module(FourLetterPHatDriver.MODULE_I2C_DEV)

    def _uninstall(self, params=None):
        """
        Uninstall driver
        """
        # do not disable i2c if other driver needs it, so there is nothing to do
        pass

    def is_installed(self):
        """
        Is driver installed ?

        Returns:
            bool: True if driver is installed
        """
        return self.config_txt.is_i2c_enabled() and self.etc_modules.is_module_enabled(FourLetterPHatDriver.MODULE_I2C_DEV)

