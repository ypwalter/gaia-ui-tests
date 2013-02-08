# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base


class Dialer(Base):

    name = "Phone"
    url = ""

    #locators
    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _call_bar_locator = ('id', 'keypad-callbar-call-action')

    def launch(self):
        self.apps.launch(self.name, url=self.url)
        self.wait_for_element_displayed(*self._keyboard_container_locator)

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
                self.marionette.tap(self.marionette.find_element('css selector', 'div.keypad-key[data-value="%s"]' % i))
                time.sleep(0.25)

    def tap_call_button(self):
        call_button = self.marionette.find_element(*self._call_bar_locator)
        self.marionette.tap(call_button)
        from gaiatest.apps.dialer.call_screen import CallScreen
        return CallScreen(self.marionette, dialing_app=self)

    @property
    def phone_number_view_value(self):
        return self.marionette.find_element(*self._phone_number_view_locator).get_attribute('value')
