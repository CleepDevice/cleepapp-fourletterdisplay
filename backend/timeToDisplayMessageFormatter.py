#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleep.libs.internals.profileformatter import ProfileFormatter
from cleep.profiles.displayMessageProfile import DisplayMessageProfile

class TimeToDisplayMessageFormatter(ProfileFormatter):
    """
    parameters.time.now event to display message profile formatter
    """
    def __init__(self, params):
        """
        Constructor

        Args:
            params (dict): formatter parameters
        """
        ProfileFormatter.__init__(self, params, 'parameters.time.now', DisplayMessageProfile())

    def _fill_profile(self, event_params, profile):
        """
        Fill profile with event values
        """
        profile.message = '%02d%02d' % (event_params['hour'], event_params['minute'])

        return profile

