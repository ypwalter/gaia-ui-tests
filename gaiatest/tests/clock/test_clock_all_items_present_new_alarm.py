# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockTestAllItemsPresentNewAlarm(GaiaTestCase):
    
    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the Clock app
        self.app = self.apps.launch('Clock')
        
        
    def test_all_items_present_new_alarm(self):

        # Wait for the new alarm screen to load
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        picker_container_tagname = self.marionette.find_element(*clock_object._picker_container).tag_name
        alarm_name_txt = self.marionette.find_element(*clock_object._alarm_name).text
        repeat_selector_txt = self.marionette.find_element(*clock_object._repeat_menu).text
        sound_selector_txt = self.marionette.find_element(*clock_object._sound_menu).text
        snooze_selector_txt = self.marionette.find_element(*clock_object._snooze_menu).text
        
        # Ensure that the picker container exists and is displayed
        self.assertEquals(picker_container_tagname, 'div',
            'Container was %s' % picker_container_tagname)
        self.assertTrue(self.marionette.find_element(*clock_object._picker_container)
            .is_displayed(), 'Picker container not displayed.')

        # Ensure the alarm name input has the default text Alarm
        self.assertEquals(alarm_name_txt, 'Alarm',
            'Alarm name was %s' % alarm_name_txt)

        # If either Never is not the text or it does not exist the below will fail
        self.assertEquals(repeat_selector_txt, 'Never',
            'Actual repeat selector text: %s' % repeat_selector_txt)

        # If either Classic is not the text or it does not exist the below will fail
        self.assertEquals(sound_selector_txt, 'Classic',
            'Actual sound selector text: %s' % sound_selector_txt)

        # If either 5 minutes is not the text or it does not exist the below will fail
        self.assertEquals(snooze_selector_txt, '5 minutes',
            'Actual snooze selector text: %s' % snooze_selector_txt)
        
        
    def tearDown(self):
        
        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
