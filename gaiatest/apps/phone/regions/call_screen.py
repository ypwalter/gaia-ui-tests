# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.phone.app import Phone


class CallScreen(Phone):

    _call_screen_locator = ('css selector', "iframe[name='call_screen']")

    _calling_number_locator = ('css selector', "div.number")
    _outgoing_call_locator = ('css selector', 'div.direction.outgoing')
    _hangup_bar_locator = ('id', 'callbar-hang-up-action')

    def __init__(self, marionette, dialing_app):
        Phone.__init__(self, marionette)
        self.dialing_app = dialing_app

        self.marionette.switch_to_frame()

        self.wait_for_element_present(*self._call_screen_locator, timeout=30)

        call_screen = self.marionette.find_element(*self._call_screen_locator)
        self.marionette.switch_to_frame(call_screen)

    @property
    def outgoing_calling_number(self):
        return self.marionette.find_element(*self._calling_number_locator).text

    def wait_for_outgoing_call(self):
        self.wait_for_element_displayed(*self._outgoing_call_locator)

    def tap_hang_up(self):
        hang_up = self.marionette.find_element(*self._hangup_bar_locator)
        self.marionette.tap(hang_up)

    def hang_up(self):
        self.tap_hang_up()
        self.marionette.switch_to_frame()
        self.wait_for_condition(lambda m:
                                self.marionette.execute_script("return window.navigator.mozTelephony.active;") is None,
                                timeout=30)
