# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from gaiatest.tests.clock import clock_object
import time

class TestClockSetAlarmTime(GaiaTestCase):
    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Clock app
        self.app = self.apps.launch('Clock')

        # delete any existing alarms
        self.data_layer.delete_all_alarms()

    def test_clock_set_alarm_time(self):
        """ Modify the alarm time

        https://moztrap.mozilla.org/manage/case/1784/

        """
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

        # create a new alarm
        alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
        self.marionette.tap(alarm_create_new)

        time.sleep(1)

        # set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.clear()
        alarm_label.send_keys("TestSetAlarmTime")

        # save the alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        time.sleep(2)
        # Get the old text for alarm
        self.wait_for_element_displayed(*clock_object._alarm_label)

        alarm_list=self.marionette.find_elements(*clock_object._all_alarms)
        old_alarm_text = alarm_list[0].text

        # Tap to Edit alarm
        alarm_item = self.marionette.find_element(*clock_object._alarm_item)
        self.marionette.tap(alarm_item)

        #Set alarm time
        self._change_hour()
        self._change_minute()
        self._change_hour24()

        #Save the alarm
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        # Verify Result
        time.sleep(2)
        self.wait_for_element_displayed(*clock_object._alarm_label)

        # Get the number of alarms set after the new alarm was added
        alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

        # Ensure that there is only one alarm
        self.assertEqual(1, alarms_count)

        # Verify label
        alarm_label = self.marionette.find_element(*clock_object._alarm_label)
        self.assertEqual("TestSetAlarmTime", alarm_label.text)

        # Verify that alarm time has been changed
        alarm_list=self.marionette.find_elements(*clock_object._all_alarms)
        new_alarm_text = alarm_list[0].text
        self.assertNotEqual(old_alarm_text, new_alarm_text)

    def _change_hour(self):
        # Get currently active hour
        active_hour = self.marionette.find_element('css selector','#value-picker-hours div[class="picker-unit active"]')
        active_hour_x_centre = int(active_hour.size['width'] / 2)
        active_hour_y_centre = int(active_hour.size['height'] / 2)
        # Get the end position from the demo animation
        value_picker_area = self.marionette.find_element(*clock_object._picker_container)
        end_animation_position = value_picker_area.size['height'] - active_hour.size['height']
        # Flick to change time
        if int(active_hour.text) < 6:
            self.marionette.flick(active_hour, active_hour_x_centre, active_hour_y_centre,  active_hour_x_centre,0-end_animation_position , 800)
        else:
            self.marionette.flick(active_hour, active_hour_x_centre, active_hour_y_centre, active_hour_x_centre,  end_animation_position , 800)
        # sleep for 1 second
        time.sleep(1)

    def _change_minute(self):
        # Get currently active minute
        active_minute = self.marionette.find_element('css selector','#value-picker-minutes div[class="picker-unit active"]')
        active_minute_x_centre = int(active_minute.size['width'] / 2)
        active_minute_y_centre = int(active_minute.size['height'] / 2)
        # Get the end position from the demo animation
        value_picker_area = self.marionette.find_element(*clock_object._picker_container)
        end_animation_position = value_picker_area.size['height'] - active_minute.size['height']
        # Flick to change time
        if int(active_minute.text) < 30:
            self.marionette.flick(active_minute, active_minute_x_centre, active_minute_y_centre,  active_minute_x_centre, 0-end_animation_position, 800)
        else:
            self.marionette.flick(active_minute, active_minute_x_centre, active_minute_y_centre,  active_minute_x_centre, end_animation_position, 800)
        # sleep for 1 second
        time.sleep(1)

    def _change_hour24(self):
        # Get currently active hour24
        active_hour24 = self.marionette.find_element('css selector','#value-picker-hour24-state div[class="picker-unit active"]')
        active_hour24_x_centre = int(active_hour24.size['width'] / 2)
        active_hour24_y_centre = int(active_hour24.size['height'] / 2)
        # Get the end position from the demo animation
        value_picker_area = self.marionette.find_element(*clock_object._picker_container)
        end_animation_position = value_picker_area.size['height'] - active_hour24.size['height']
        # Flick to change time
        if active_hour24.text == 'AM':
            self.marionette.flick(active_hour24, active_hour24_x_centre, active_hour24_y_centre,  active_hour24_x_centre , 0-end_animation_position,800)
        else:
            self.marionette.flick(active_hour24, active_hour24_x_centre, active_hour24_y_centre, active_hour24_x_centre, end_animation_position,  800)
        # sleep for 1 second
        time.sleep(1)

    def tearDown(self):
        # delete any existing alarms
        self.data_layer.delete_all_alarms()

        GaiaTestCase.tearDown(self)
