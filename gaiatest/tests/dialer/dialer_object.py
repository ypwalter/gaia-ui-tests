# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time


# Dialer app
_keyboard_container_locator = ('id', 'keyboard-container')
_phone_number_view_locator = ('id', 'phone-number-view')
_call_bar_locator = ('id', 'keypad-callbar-call-action')

# Call Screen app
_calling_number_locator = ('css selector', "div.number")
_outgoing_call_locator = ('css selector', 'div.direction.outgoing')
_hangup_bar_locator = ('id', 'callbar-hang-up-action')
_call_screen_locator = ('css selector', "iframe[name='call_screen']")

def wait_for_ready_to_dial(self):
    self.wait_for_element_displayed(*_keyboard_container_locator)

def dial_number(self, phone_number):
    '''
    Dial a number using the keypad
    '''

    for i in phone_number:
        if i == "+":
            zero_button = self.marionette.find_element('css selector', 'div.keypad-key[data-value="0"]')
            self.marionette.long_press(zero_button, 1200)
            # Wait same time as the long_press to bust the asynchronous
            # TODO https://bugzilla.mozilla.org/show_bug.cgi?id=815115
            time.sleep(2)

        else:
            self.marionette.find_element('css selector', 'div.keypad-key[data-value="%s"]' % i).click()
            time.sleep(0.25)

def place_call(self):
    # Click the call button
    self.marionette.find_element(*_call_bar_locator).click()

    # Switch to top level frame
    self.marionette.switch_to_frame()

    # Wait for call screen then switch to it
    self.wait_for_element_present(*_call_screen_locator, timeout=30)
    call_screen = self.marionette.find_element(*_call_screen_locator)
    self.marionette.switch_to_frame(call_screen)

    # Wait for call screen to be dialing
    self.wait_for_element_displayed(*_outgoing_call_locator)

    # Wait for the state to get to 'alerting' which means connection made
    self.wait_for_condition(lambda m: self.data_layer.active_telephony_state == "alerting", timeout=30)

def hang_up(self):
    # hang up before the person answers ;)
    self.marionette.find_element(*_hangup_bar_locator).click()

def create_alarm(self):
    """ create a new alarm for test """
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    # find the origin alarms' number
    initial_alarms_count = len(self.marionette.find_elements(*_all_alarms))
    self.marionette.find_element(*_alarm_create_new_locator).click()
    self.marionette.find_element(*_alarm_save_locator).click()
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    self.wait_for_condition(lambda m: len(m.find_elements(*_all_alarms)) > initial_alarms_count)

def delete_alarm(self):
    """ delete the new alarm """
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    # find the origin alarms' number
    initial_alarms_count = len(self.marionette.find_elements(*_all_alarms))
    self.marionette.find_element(*_alarm_item).click()
    self.marionette.find_element(*_alarm_delete_button).click()
    self.wait_for_element_displayed(*_alarm_create_new_locator)
    self.wait_for_condition(lambda m: len(m.find_elements(*_all_alarms)) < initial_alarms_count)
