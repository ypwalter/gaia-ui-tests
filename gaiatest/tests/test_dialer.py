# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestDialer(GaiaTestCase):

    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _call_bar_locator = ('id', 'keypad-callbar-call-action')
    _hangup_bar_locator = ('id', 'callbar-hang-up-action')
    _call_screen_locator = ('css selector', "iframe[name='call_screen']")

    _test_phone_number = "+1234567890"

    def setUp(self):

        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # set audio volume to 0
        self.data_layer.set_volume(0)

        # launch the app
        self.app = self.apps.launch('Phone')

    def test_dialer_make_call(self):
        # https://moztrap.mozilla.org/manage/case/1298/

        self.wait_for_element_displayed(*self._keyboard_container_locator)

        self._dial_number(self._test_phone_number)

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(
            *self._phone_number_view_locator)

        self.assertEqual(
            phone_view.get_attribute('value'), self._test_phone_number)

        # Now press call!
        # TODO before this step we need to use a real phone number passed in by testvars
        #self.marionette.find_element(*self._call_bar_locator).click()

        #self.marionette.switch_to_frame()

        # Wait for call screen
        #self.wait_for_element_present(*self._call_screen_locator)
        #call_screen = self.marionette.find_element(*self._call_screen_locator)

        # TODO this does not work yet
        #self.marionette.switch_to_frame(call_screen)

        # TODO assert that it is ringing
        #self.assertTrue(ringing)

        # hang up
        #self.marionette.find_element(*self._hangup_bar_locator).click()

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)

    def _dial_number(self, phone_number):
        '''
        Dial a number using the keypad
        '''

        for i in phone_number:
            if i == "+":
                zero_button = self.marionette.find_element('css selector', 'div.keypad-key div[data-value="0"]')
                self.marionette.long_press(zero_button, 1200)
                # Wait same time as the long_press to bust the asynchronous
                # TODO https://bugzilla.mozilla.org/show_bug.cgi?id=815115
                time.sleep(2)

            else:
                self.marionette.find_element('css selector', 'div.keypad-key div[data-value="%s"]' % i).click()
                time.sleep(0.25)
