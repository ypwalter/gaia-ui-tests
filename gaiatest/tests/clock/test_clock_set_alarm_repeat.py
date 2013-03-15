# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockSetAlarmRepeat(GaiaTestCase):

    _alarm_repeat_menu_locator = ('id','repeat-menu')
    _alarm_repeat_select_locator = ('css selector','#value-selector-container li')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    def test_clock_set_alarm_repeat(self):
        """ Modify the alarm repeat

        https://moztrap.mozilla.org/manage/case/1786/
        Test that [Clock][Alarm] Change the repeat state

        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        # create a new alarm
        alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
        self.marionette.tap(alarm_create_new)

        # Hack job on this, track Bug 830197
        time.sleep(1)

        # Set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.clear()
        alarm_label.send_keys("TestSetAlarmRepeat")

        # Set alarm repeat
        self.wait_for_element_displayed(*self._alarm_repeat_menu_locator)
        alarm_repeat_menu=self.marionette.find_element(*self._alarm_repeat_menu_locator)	
        self.marionette.tap(alarm_repeat_menu)

        # Go back to top level to get B2G select box wrapper
        self.marionette.switch_to_frame()

        # get the list of repeat options
        repeat_options=self.marionette.find_elements(*self._alarm_repeat_select_locator)

        # loop the options and select the ones in match list
        match_list = 'Monday Tuesday Wednesday Thursday Friday'
        for ro in repeat_options:
            if ro.text in match_list:
               self.marionette.tap(ro)
        # test click twice
            if ro.text=='Saturday':
               self.marionette.tap(ro)
               self.marionette.tap(ro)

        # Click OK
        ok_button=self.marionette.find_element('css selector','button.value-option-confirm')
        self.marionette.tap(ok_button)

        # Switch back to app
        self.marionette.switch_to_frame(self.app.frame)
        
        # Save the alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        time.sleep(1)
        # Go to details page again
        self.wait_for_element_displayed(*clock_object._alarm_label)
        alarm_list=self.marionette.find_elements(*clock_object._all_alarms)

        # Tap to Edit alarm
        alarm_label = self.marionette.find_element(*clock_object._alarm_label)
        self.marionette.tap(alarm_label)

        # To verify the select list. 
        self.wait_for_element_displayed(*self._alarm_repeat_menu_locator)
        alarm_repeat_menu=self.marionette.find_element(*self._alarm_repeat_menu_locator)
        self.assertEqual("Weekdays" , alarm_repeat_menu.text)

        # Close alarm
        alarm_close = self.marionette.find_element(*clock_object._alarm_close)
        self.marionette.tap(alarm_close)

    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)
