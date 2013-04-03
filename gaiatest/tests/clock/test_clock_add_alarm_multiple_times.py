# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockAddAlarmMultipleTimes(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Clock app
        self.app = self.apps.launch('Clock')

        # delete any existing alarms
        self.data_layer.delete_all_alarms()

    def test_clock_add_alarm_multiple_times(self):
        """ Add multiple alarm

        https://moztrap.mozilla.org/manage/case/1773/

        """

        "Add multiple alarms"
        count = 3
        for x in range(count):
            self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

            # create a new alarm with the default values that are available
            alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
            self.marionette.tap(alarm_create_new)

            self.wait_for_element_displayed(*clock_object._alarm_save_locator)
            alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
            self.marionette.tap(alarm_save)

            # verify the banner-countdown message appears
            self.wait_for_element_displayed(*clock_object._banner_countdown_notification_locator)
            alarm_msg = self.marionette.find_element(*clock_object._banner_countdown_notification_locator).text
            self.assertIn('The alarm is set for',alarm_msg)

            # Get the number of alarms set after the new alarm was added
            new_alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

            # Ensure the new alarm has been added and is displayed
            self.assertEqual(x+1, new_alarms_count)
            # sleep for a while until the alarm message disappear
            time.sleep(5)

    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)
