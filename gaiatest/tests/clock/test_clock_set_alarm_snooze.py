# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockSetAlarmSnooze(GaiaTestCase):

    _alarm_snooze_menu_locator= ('id','snooze-menu')
    _alarm_snoozes_locator=('css selector','#value-selector-container li')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    def test_clock_set_alarm_snooze(self):
        """ Modify the alarm snooze
	
        Test that [Clock][Alarm] Change the snooze time

        https://moztrap.mozilla.org/manage/case/1788/

        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        # create a new alarm
        alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
        self.marionette.tap(alarm_create_new)

        # Hack job on this
        time.sleep(1)

        # set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.clear()
        alarm_label.send_keys("TestSetAlarmSnooze")

        #select snooze
        self.wait_for_element_displayed(*self._alarm_snooze_menu_locator)
        alarm_snooze_menu=self.marionette.find_element(*self._alarm_snooze_menu_locator)	
        self.marionette.tap(alarm_snooze_menu)

        # Go back to top level to get B2G select box wrapper
        self.marionette.switch_to_frame()
        alarm_snoozes=self.marionette.find_elements(*self._alarm_snoozes_locator)

        # loop the options and set to 15 minutes
        for ro in alarm_snoozes:
            if ro.text=='15 minutes':
               self.marionette.tap(ro)
               break
        # Click OK
        ok_button=self.marionette.find_element('css selector','button.value-option-confirm')
        self.marionette.tap(ok_button)

        # Switch back to app
        self.marionette.switch_to_frame(self.app.frame)

        # save alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        time.sleep(1)
        # Go to details page again
        self.wait_for_element_displayed(*clock_object._alarm_label)
        alarm_list=self.marionette.find_elements(*clock_object._all_alarms)

        # Tap to Edit alarm
        alarm_label = self.marionette.find_element(*clock_object._alarm_label)
        self.marionette.tap(alarm_label)

        # to verify the select list.
        self.wait_for_element_displayed(*self._alarm_snooze_menu_locator)
        alarm_snooze_menu=self.marionette.find_element(*self._alarm_snooze_menu_locator)
        self.assertEqual("15 minutes", alarm_snooze_menu.text)

        # Close alarm
        alarm_close = self.marionette.find_element('id','alarm-close')
        self.marionette.tap(alarm_close)

    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)


