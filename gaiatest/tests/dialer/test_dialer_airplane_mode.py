# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.phone.app import Phone

class TestDialerAirplaneMode(GaiaTestCase):

    _dialog_locator = ('id', 'confirmation-message')
    _dialog_title_locator = ('xpath', "//h1[text()='Airplane mode activated']")

    def setUp(self):

        GaiaTestCase.setUp(self)

    def test_dialer_airplane_mode(self):
        # https://moztrap.mozilla.org/manage/case/2282/
        
        # Disable the device radio, enable Airplane mode
        self.data_layer.set_setting('ril.radio.disabled', True)

        # Check that we are in Airplane mode
        self.assertTrue(self.data_layer.get_setting('ril.radio.disabled'))

        # Launch the device dialer
        phone = Phone(self.marionette)
        phone.launch()

        # Make a call
        test_phone_number = self.testvars['remote_phone_number']
        phone.keypad.call_number(test_phone_number)

        # Check for the Airplane mode dialog
        self.wait_for_element_displayed(*self._dialog_locator)
        self.wait_for_element_displayed(*self._dialog_title_locator)

    def tearDown(self):

        GaiaTestCase.tearDown(self)
