# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.clock.app import Clock


class NewAlarm(Clock):

    _picker_container_locator = ('id', 'picker-container')
    _alarm_name_locator = ('xpath', "//input[@placeholder='Alarm']")
    _repeat_menu_locator = ('id', 'repeat-menu')
    _sound_menu_locator = ('id', 'sound-menu')
    _snooze_menu_locator = ('id', 'snooze-menu')
    _done_locator = ('id', 'alarm-done')

    @property
    def alarm_label(self):
        return self.marionette.find_element(*self._alarm_name_locator).text

    def type_alarm_label(self, value):
        label = self.marionette.find_element(*self._alarm_name_locator)
        label.clear()
        label.send_keys(value)

    @property
    def alarm_label_placeholder(self):
        return self.marionette.find_element(*self._alarm_name_locator).get_attribute('placeholder')

    @property
    def alarm_repeat(self):
        return self.marionette.find_element(*self._repeat_menu_locator).text

    @property
    def alarm_snooze(self):
        return self.marionette.find_element(*self._snooze_menu_locator).text

    @property
    def alarm_sound(self):
        return self.marionette.find_element(*self._sound_menu_locator).text

    def wait_for_picker_to_be_visible(self):
        self.wait_for_element_displayed(*self._picker_container_locator)

    def tap_done(self):
        self.marionette.tap(self.marionette.find_element(*self._done_locator))

        clock = Clock(self.marionette)
        clock.wait_for_banner_displayed()
        return clock


class EditAlarm(NewAlarm):

    _alarm_delete_button_locator = ('id', 'alarm-delete')

    def __init__(self, marionette):
        NewAlarm.__init__(self, marionette)
        self.wait_for_element_displayed(*self._alarm_delete_button_locator)

    def tap_delete(self):
        self.marionette.tap(self.marionette.find_element(*self._alarm_delete_button_locator))
        return Clock(self.marionette)
