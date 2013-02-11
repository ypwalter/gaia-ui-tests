# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from gaiatest.apps.dialer.dialer import Dialer


class TestDialer(GaiaTestCase):

    def test_dialer_make_call(self):
        # https://moztrap.mozilla.org/manage/case/1298/

        test_phone_number = self.testvars['twilio']['phone_number']

        dialer = Dialer(self.marionette)
        dialer.launch()

        dialer.dial_number(test_phone_number)

        # Assert that the number was entered correctly.
        self.assertEqual(dialer.phone_number_view, test_phone_number)

        # Click the call button
        call_screen = dialer.tap_call_button()

        # Wait for call screen to be dialing
        call_screen.wait_for_outgoing_call()

        # Wait for the state to get to 'alerting' which means connection made
        call_screen.wait_for_condition(lambda m: self.data_layer.active_telephony_state == "alerting", timeout=30)

        # Check the number displayed is the one we dialed
        self.assertEqual(test_phone_number, call_screen.outgoing_calling_number)

    def tearDown(self):

        # In case the assertion fails this will still kill the call
        # An open call creates problems for future tests
        self.data_layer.kill_active_call()

        GaiaTestCase.tearDown(self)
