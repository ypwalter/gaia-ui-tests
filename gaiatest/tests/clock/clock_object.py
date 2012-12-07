# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest import GaiaTestCase
from marionette import MarionetteTestCase
from marionette import Marionette
import time

_alarm_create_new_locator                       = ('id', 'alarm-new')

_clock_day_date                                 = ('id', 'clock-day-date')

_analog_clock_display                           = ('id', 'analog-clock-svg')
_analog_clock_body                              = ('id', 'analog-clock-svg-body')
_digital_clock_display                          = ('id', 'digital-clock-display')
_digital_clock_body                             = ('id', 'clock-time')
    
_alarm_save_locator                             = ('id', 'alarm-done')
_banner_countdown_notification_locator          = ('id', 'banner-countdown')

_alarm_checked_status                           = ('css selector', 'li label.alarmList #input-enable')
_alarm_checked_status_button                    = ('css selector', 'li label.alarmList')

_alarm_item                                     = ('id', 'alarm-item')
_alarm_delete_button                            = ('id', 'alarm-delete')
_alarms_list                                    = ('css selector', 'ul#alarms li')

def create_alarm(self):
    """ create a new alarm for test """
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    self.marionette.find_element(*_alarm_create_new_locator).click()
    self.marionette.find_element(*_alarm_save_locator).click()
    time.sleep(2)

def delete_alarm(self):
    """ delete the new alarm """
    self.marionette.find_element(*_alarm_item).click()
    self.marionette.find_element(*_alarm_delete_button).click()
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    time.sleep(2)
    