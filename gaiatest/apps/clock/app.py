# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base, PageRegion


class Clock(Base):

    name = "Clock"

    _alarm_create_new_locator = ('id', 'alarm-new')

    _analog_clock_display = ('id', 'analog-clock-svg')
    _digital_clock_display = ('id', 'digital-clock-display')
    _clock_day_date = ('id', 'clock-day-date')
    _digital_clock_hour24_state = ('id', 'clock-hour24-state')

    _all_alarms = ('css selector', '#alarms li')

    _banner_countdown_notification_locator = ('id', 'banner-countdown')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

    @property
    def is_digital_clock_displayed(self):
        return self.is_element_displayed(*self._digital_clock_display)

    @property
    def is_analog_clock_displayed(self):
        return self.is_element_displayed(*self._analog_clock_display)

    @property
    def is_day_and_date_displayed(self):
        return self.is_element_displayed(*self._clock_day_date)

    @property
    def is_24_hour_state_displayed(self):
        return self.is_element_displayed(*self._digital_clock_hour24_state)

    @property
    def number_of_set_alarms(self):
        return len(self.marionette.find_elements(*self._all_alarms))

    @property
    def banner_countdown_notification(self):
        return self.marionette.find_element(*self._banner_countdown_notification_locator).text

    @property
    def alarms(self):
        return [self.Alarm(self.marionette, alarm) for alarm in self.marionette.find_elements(*self._all_alarms)]

    def launch(self):
        Base.launch(self)
        self.wait_for_new_alarm_button()

    def wait_for_new_alarm_button(self):
        self.wait_for_element_displayed(*self._alarm_create_new_locator)

    def wait_for_banner_not_visible(self):
        self.wait_for_element_not_displayed(*self._banner_countdown_notification_locator)

    def wait_for_banner_displayed(self):
        self.wait_for_element_displayed(*self._banner_countdown_notification_locator)

    def tap_analog_display(self):
        self.marionette.tap(self.marionette.find_element(*self._analog_clock_display))
        self.wait_for_element_displayed(*self._digital_clock_display)

    def tap_digital_display(self):
        self.marionette.tap(self.marionette.find_element(*self._digital_clock_display))
        self.wait_for_element_displayed(*self._analog_clock_display)

    def tap_new_alarm(self):
        self.marionette.tap(self.marionette.find_element(*self._alarm_create_new_locator))

        from gaiatest.apps.clock.regions.alarm import NewAlarm
        new_alarm = NewAlarm(self.marionette)
        new_alarm.wait_for_picker_to_be_visible()

        return new_alarm

    class Alarm(PageRegion):

        _label_locator = ('css selector', 'div.label')
        _tap_locator = ('id', 'alarm-item')
        _check_box_locator = ('id', 'input-enable')
        _enable_button_locator = ('css selector', 'label.alarmList')

        @property
        def label(self):
            return self.root_element.find_element(*self._label_locator).text

        @property
        def is_alarm_active(self):
            return self.root_element.find_element(*self._check_box_locator).is_selected()

        def tap_checkbox(self):
            self.marionette.tap(self.root_element.find_element(*self._enable_button_locator))

        def tap(self):
            self.marionette.tap(self.root_element.find_element(*self._tap_locator))
            from gaiatest.apps.clock.regions.alarm import Edit_Alarm
            return Edit_Alarm(self.marionette)
