# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from twilio.rest import TwilioRestClient
from gaiatest import GaiaTestCase


class TestCallLog(GaiaTestCase):

    _incoming_call_frame_locator = ('css selector', 'iframe[name="call_screen"]')
    _incoming_call_number_locator = ('id', 'incoming-number')

    _recent_calls_toolbar_button_locator = ('id', 'option-recents')

    _all_calls_log_tab_locator = ('id', 'allFilter')
    _all_calls_log_button_locator = ('css selector', '#allFilter a')
    _missed_calls_log_tab_locator = ('id', 'missedFilter')
    _missed_calls_log_button_locator = ('css selector', '#missedFilter a')

    _all_calls_list_item = ('css selector', 'li.log-item')
    _missed_call_list_item = (
        'css selector', "li.log-item[data-type='incoming-refused']")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Make a call to the phone with Twilio
        self.place_call_with_twilio(self.testvars['this_phone_number'])

        # launch the app
        self.app = self.apps.launch('Phone')

    def test_call_log_missed_calls(self):
        # https://moztrap.mozilla.org/manage/case/1306/

        self.wait_for_element_displayed(
            *self._recent_calls_toolbar_button_locator)

        self.marionette.tap(self.marionette.find_element(
            *self._recent_calls_toolbar_button_locator))

        self.wait_for_element_displayed(*self._missed_calls_log_tab_locator)
        missed_calls_tab = self.marionette.find_element(*self._missed_calls_log_tab_locator)
        self.marionette.tap(self.marionette.find_element(*self._missed_calls_log_button_locator))
        self.wait_for_condition(lambda m: missed_calls_tab.get_attribute('class') == 'selected')

        # Check that 'Missed calls' tab is selected
        self.assertEqual(missed_calls_tab.get_attribute('class'), 'selected')

        # Now check that at least one call is listed.
        missed_calls = self.marionette.find_elements(
            *self._missed_call_list_item)

        self.assertGreater(len(missed_calls), 0)

        # Check that the first one is displayed. this is only a smoke test after all
        self.assertTrue(missed_calls[0].is_displayed())

    def test_call_log_all_calls(self):
        # https://moztrap.mozilla.org/manage/case/1306/

        self.wait_for_element_displayed(
            *self._recent_calls_toolbar_button_locator)

        self.marionette.tap(self.marionette.find_element(
            *self._recent_calls_toolbar_button_locator))

        self.wait_for_element_displayed(*self._all_calls_log_tab_locator)
        all_calls_tab = self.marionette.find_element(*self._all_calls_log_tab_locator)
        self.marionette.tap(self.marionette.find_element(*self._all_calls_log_button_locator))
        self.wait_for_condition(lambda m: all_calls_tab.get_attribute('class') == 'selected')

        # Check that 'All calls' tab is selected
        self.assertEqual(all_calls_tab.get_attribute('class'), 'selected')

        # Now check that at least one call is listed.
        all_calls = self.marionette.find_elements(*self._all_calls_list_item)

        self.assertGreater(len(all_calls), 0)

        # Check that the first one is displayed. this is only a smoke test after all
        self.assertTrue(all_calls[0].is_displayed())

    def place_call_with_twilio(self, number):

        # Twilio credentials
        account_sid = self.testvars['twilio_account_sid']
        auth_token = self.testvars['twilio_auth_token']

        client = TwilioRestClient(account_sid, auth_token)

        # Make the call
        call = client.calls.create(to=number, # This phone number
            from_=self.testvars['twilio_phone_number'], # Must be a valid Twilio number
            url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
        sid = call.sid
        call = client.calls.get(sid)

        # wait to connect
        self.marionette.switch_to_frame()
        frame = self.marionette.find_element(*self._incoming_call_frame_locator)
        self.marionette.switch_to_frame(frame)
        self.wait_for_element_displayed(*self._incoming_call_number_locator)

        # stop call
        call.hangup()

