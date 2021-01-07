#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import logging
import sys
sys.path.append('../')
from backend.fourletterdisplay import Fourletterdisplay
from cleep.exception import InvalidParameter, MissingParameter, CommandError, Unauthorized
from cleep.libs.tests import session
from mock import Mock, patch

class TestFourletterdisplay(unittest.TestCase):

    def setUp(self):
        self.session = session.TestSession(self)
        logging.basicConfig(level=logging.FATAL, format=u'%(asctime)s %(name)s:%(lineno)d %(levelname)s : %(message)s')

    def tearDown(self):
        #clean session
        self.session.clean()

    def init_session(self, start=True):
        self.module = self.session.setup(Fourletterdisplay)
        if start:
            self.session.start_module(self.module)

    def test_my_test(self):
        self.init_session(False)
        self.module.set_brightness = Mock()

        self.session.start_module(self.module)

        self.module.set_brightness.assert_called_with(15)

if __name__ == '__main__':
    # coverage run --omit="*lib/python*/*","test_*" --concurrency=thread test_fourletterdisplay.py; coverage report -m -i
    unittest.main()
    
