# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.clock.app import Clock


class NewAlarm(Clock):

    _picker_container = ('id', 'picker-container')
    _alarm_name = ('xpath', "//input[@placeholder='Alarm']")
    _repeat_menu = ('id', 'repeat-menu')
    _sound_menu = ('id', 'sound-menu')
    _snooze_menu = ('id', 'snooze-menu')

    _done_locator = ('id', 'alarm-done')

    @property
    def alarm_label(self):
        return self.marionette.find_element(*self._alarm_name).text

    @alarm_label.setter
    def alarm_label(self, value):
        label = self.marionette.find_element(*self._alarm_name)
        label.clear()
        label.send_keys(value)

    @property
    def alarm_label_placeholder(self):
        return self.marionette.find_element(*self._alarm_name).get_attribute('placeholder')

    @property
    def alarm_repeat(self):
        return self.marionette.find_element(*self._repeat_menu).text

    @property
    def alarm_snooze(self):
        return self.marionette.find_element(*self._snooze_menu).text

    @property
    def alarm_sound(self):
        return self.marionette.find_element(*self._sound_menu).text

    def wait_for_picker_to_be_visible(self):
        self.wait_for_element_displayed(*self._picker_container)

    def tap_done(self):
        self.marionette.tap(self.marionette.find_element(*self._done_locator))

        clock = Clock(self.marionette)
        clock.wait_for_banner_displayed()
        return clock


class Edit_Alarm(NewAlarm):

    _alarm_delete_button = ('id', 'alarm-delete')

    def __init__(self, marionette):
        NewAlarm.__init__(self, marionette)
        self.wait_for_element_displayed(*self._alarm_delete_button)

    def tap_delete(self):
        self.marionette.tap(self.marionette.find_element(*self._alarm_delete_button))
        return Clock(self.marionette)
