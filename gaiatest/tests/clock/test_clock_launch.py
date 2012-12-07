# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockLaunch(GaiaTestCase):
    
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    def test_clock_launch(self):
        """ Launch the Clock
        
        https://moztrap.mozilla.org/manage/case/1769/
        
        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)
        self.assertTrue(self.marionette.find_element(*clock_object._clock_day_date).is_displayed(), "The Day field should be displayed.")
        
        
    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
