# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.phone.app import Phone


class TestCallLogAllCalls(GaiaTestCase):

    def test_call_log_all_calls(self):
        # https://moztrap.mozilla.org/manage/case/1306/

        phone = Phone(self.marionette)
        phone.launch()
        test_phone_number = self.testvars['remote_phone_number']

        # Make a call so it will appear in the call log
        self._make_outgoing_call(phone, test_phone_number)

        # Switch back to phone app
        phone.launch()
        call_log = phone.tap_call_log_toolbar_button()

        call_log.tap_all_calls_tab()

        # Check that 'All calls' tab is selected
        self.assertTrue(call_log.is_all_calls_tab_selected)

        # Now check that at least one call is listed.
        self.assertGreater(call_log.all_calls_count, 0)

        # Check that the call displayed is for the call we made
        self.assertIn(test_phone_number, call_log.first_all_call_text)

    def _make_outgoing_call(self, phone, test_phone_number):

        call_screen = phone.keypad.call_number(test_phone_number)
        call_screen.wait_for_outgoing_call()
        call_screen.hang_up()

    def tearDown(self):

        # In case the assertion fails this will still kill the call
        # An open call creates problems for future tests
        self.data_layer.kill_active_call()

        # delete any existing call log entries
        self.data_layer.delete_all_call_log_entries()

        GaiaTestCase.tearDown(self)
