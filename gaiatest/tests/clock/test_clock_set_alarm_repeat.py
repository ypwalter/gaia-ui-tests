# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

_alarm_repeat_menu = ('id','repeat-menu')
_alarm_repeat_select = ('id','repeat-select')
_alarm_repeat_mon = ('css selector','#repeat-select option[data-l10n-id="weekday-1-long"]')
_alarm_repeat_tue = ('css selector','#repeat-select option[data-l10n-id="weekday-2-long"]')
_alarm_repeat_wed = ('css selector','#repeat-select option[data-l10n-id="weekday-3-long"]')
_alarm_repeat_thu = ('css selector','#repeat-select option[data-l10n-id="weekday-4-long"]')
_alarm_repeat_fri = ('css selector','#repeat-select option[data-l10n-id="weekday-5-long"]')
_alarm_repeat_sat = ('css selector','#repeat-select option[data-l10n-id="weekday-6-long"]')

class TestClockSetAlarmRepeat(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

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

        # set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.send_keys("\b\b\b\b\btestrepeat")

        #set alarm repeat
        self.wait_for_element_displayed(*_alarm_repeat_menu)
        alarm_repeat_menu=self.marionette.find_element(*_alarm_repeat_menu)	
        self.marionette.tap(alarm_repeat_menu)
	
        #add monday
        alarm_repeat_mon=self.marionette.find_element(*_alarm_repeat_mon)
        #self.marionette.tap(alarm_repeat_mon)
        alarm_repeat_mon.click()
        time.sleep(1)

        #add tuesday
        alarm_repeat_tue=self.marionette.find_element(*_alarm_repeat_tue)
        alarm_repeat_tue.click()
        #print alarm_repeat_tue.text
	
        #add wednesday
        alarm_repeat_wed=self.marionette.find_element(*_alarm_repeat_wed)
        alarm_repeat_wed.click()
        #print alarm_repeat_wed.text

        #add thuesday
        alarm_repeat_thu=self.marionette.find_element(*_alarm_repeat_thu)
        alarm_repeat_thu.click()

        #add friday
        alarm_repeat_fri=self.marionette.find_element(*_alarm_repeat_fri)
        alarm_repeat_fri.click()

        #Test click twice on one element
        alarm_repeat_sat=self.marionette.find_element(*_alarm_repeat_sat)
        alarm_repeat_sat.click()
        time.sleep(1)
        alarm_repeat_sat.click()

        # save the alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        # verify the label of alarm
        self.wait_for_element_displayed(*clock_object._alarm_label)

        alarm_label = self.marionette.find_element(*clock_object._alarm_label).text
        self.assertTrue("testrepeat" == alarm_label, 'Actual alarm label was: "' + alarm_label + '", not "testrepeat".')

        #TBD to verify the select list. Need more investigation.
        self.wait_for_element_displayed(*_alarm_repeat_menu)
        alarm_repeat_menu=self.marionette.find_element(*_alarm_repeat_menu)
        self.assertTrue("Weekdays" == alarm_repeat_menu.text, 'Actual alarm repeat was: "' + alarm_repeat_menu.text + '", not "Weekdays".')
        #print alarm_repeat_menu.text
        #self.assertTrue(alarm_repeat_fri.enabled(),'Friday not selected')

    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)
