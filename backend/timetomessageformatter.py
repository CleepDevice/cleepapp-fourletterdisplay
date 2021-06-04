#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleep.libs.internals.profileformatter import ProfileFormatter
from cleep.profiles.messageprofile import MessageProfile

class TimeToMessageFormatter(ProfileFormatter):
    """
    parameters.time.now event to message profile formatter
    """
    def __init__(self, params):
        """
        Constructor

        Args:
            params (dict): formatter parameters
        """
        ProfileFormatter.__init__(self, params, 'parameters.time.now', MessageProfile())

    def _fill_profile(self, event_params, profile):
        """
        Fill profile with event values
        """
        profile.message = '%02d%02d' % (event_params['hour'], event_params['minute'])

        return profile

