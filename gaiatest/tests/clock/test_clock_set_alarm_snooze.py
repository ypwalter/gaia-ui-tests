# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

_alarm_snooze_menu= ('id','snooze-menu')
_alarm_snooze_select=('id','snooze-select')
_alarm_snooze_15min=('css selector','#snooze-select option[value="15"]')
_alarm_snoozes=('css selector','#snooze-select option[data-l10n-id="nMinutes"]')

class TestClockSetAlarmSnooze(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

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
        alarm_label.send_keys("\b\b\b\b\btestsnooze")

	#select snooze

	self.wait_for_element_displayed(*_alarm_snooze_menu)
	alarm_snooze_menu=self.marionette.find_element(*_alarm_snooze_menu)	
	self.marionette.tap(alarm_snooze_menu)

	#find all options
	#alarm_snoozes=self.marionette.find_elements(*_alarm_snoozes)
	#print len(alarm_snoozes)
	
	#alarm_snooze_15min=alarm_snoozes[1]
	#print alarm_snooze_15min.text
	alarm_snooze_15min=self.marionette.find_element(*_alarm_snooze_15min)
	alarm_snooze_15min.click()


	

	#save alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

	#TBD to verify the select list. Need more investigation.
	self.wait_for_element_displayed(*_alarm_snooze_menu)
	alarm_snooze_menu=self.marionette.find_element(*_alarm_snooze_menu)
	self.assertTrue("15 minutes" == alarm_snooze_menu.text, 'Actual alarm snooze was: "' + alarm_snooze_menu.text + '", not "15 minutes".')


    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)


