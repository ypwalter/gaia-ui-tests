# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.phone.app import Phone


class CallScreen(Phone):

    _call_screen_locator = ('css selector', "iframe[name='call_screen0']")

    _calling_contact_locator = ('css selector', 'div.number')
    _calling_contact_information_locator = ('css selector', 'div.additionalContactInfo')
    _outgoing_call_locator = ('css selector', 'div.direction.outgoing')
    _hangup_bar_locator = ('id', 'callbar-hang-up-action')

    def __init__(self, marionette):
        Phone.__init__(self, marionette)

        self.marionette.switch_to_frame()

        self.wait_for_element_present(*self._call_screen_locator, timeout=30)

        call_screen = self.marionette.find_element(*self._call_screen_locator)
        self.marionette.switch_to_frame(call_screen)

    @property
    def outgoing_calling_contact(self):
        self.wait_for_element_displayed(*self._calling_contact_locator)
        return self.marionette.find_element(*self._calling_contact_locator).text

    @property
    def calling_contact_information(self):
        return self.marionette.find_element(*self._calling_contact_information_locator).text

    def wait_for_outgoing_call(self):
        self.wait_for_element_displayed(*self._outgoing_call_locator)
        self.wait_for_element_displayed(*self._calling_contact_locator)

    def tap_hang_up(self):
        hang_up = self.marionette.find_element(*self._hangup_bar_locator)
        self.marionette.tap(hang_up)

    def hang_up(self):
        self.tap_hang_up()
        self.marionette.switch_to_frame()
        self.wait_for_condition(lambda m:
                                not self.marionette.execute_script('return window.navigator.mozTelephony.active;'),
                                timeout=30)
