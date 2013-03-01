# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

_alarm_sound_menu= ('id','sound-menu')
_alarm_sound_select=('id','sound-select')
_alarm_sound_smooth_strings=('css selector','#sound-select option[data-l10n-id="ac_soft_smooth_strings_opus"]')


class TestClockSetAlarmSound(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    def test_clock_set_alarm_sound(self):
        """ Modify the alarm sound

	[Clock][Alarm] Change the alarm sound
        https://moztrap.mozilla.org/manage/case/1787/

        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        # create a new alarm
        alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
        self.marionette.tap(alarm_create_new)

        # Hack job on this
        time.sleep(1)

        # set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.send_keys("\b\b\b\b\btestsound")

	#select sound

	self.wait_for_element_displayed(*_alarm_sound_menu)
	alarm_sound_menu=self.marionette.find_element(*_alarm_sound_menu)	
	self.marionette.tap(alarm_sound_menu)

	alarm_sound_smooth_strings=self.marionette.find_element(*_alarm_sound_smooth_strings)
	alarm_sound_smooth_strings.click()

	#save alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

	#TBD to verify the select list. Need more investigation.
	self.wait_for_element_displayed(*_alarm_sound_menu)
	alarm_sound_menu=self.marionette.find_element(*_alarm_sound_menu)
	self.assertTrue("Smooth Strings" == alarm_sound_menu.text, 'Actual alarm sound was: "' + alarm_sound_menu.text + '", not "Smooth Strings".')


    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)


