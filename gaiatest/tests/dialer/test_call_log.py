# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.dialer import dialer_object


class TestCallLog(GaiaTestCase):

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

        # This test needs a remote_phone_number and a this_phone_number
        self.assertTrue(self.testvars, 'Test variables file not provided')
        self.assertTrue('remote_phone_number' in self.testvars,
            'No remote phone number present in test variables file')
        self.remote_phone_number = self.testvars['remote_phone_number']
        self.assertTrue(self.remote_phone_number,
            'Remote phone number in test variables file is empty')
        self.assertTrue('this_phone_number' in self.testvars,
            'No this phone number present in test variables file')
        self.this_phone_number = self.testvars['this_phone_number']
        self.assertTrue(self.this_phone_number,
            'This phone number in test variables file is empty')

        # TODO: Make a call to the phone (with Twilio)
        # This test will fail if no calls have been made

        # launch the app
        self.app = self.apps.launch('Phone')

    def test_call_log_all_calls(self):
        # https://moztrap.mozilla.org/manage/case/1306/

        # Place a call from the phone
        self.place_call(self.remote_phone_number)

        # Need to get back to phone app
        self.app = self.apps.launch('Phone')

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

    def place_call(self, phone_number):

        dialer_object.wait_for_ready_to_dial(self)

        dialer_object.dial_number(self, phone_number)

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(
            *dialer_object._phone_number_view_locator)

        self.assertEqual(
            phone_view.get_attribute('value'), phone_number)

        # Now press call!
        dialer_object.place_call(self)

        # Check the number displayed is the one we dialed
        self.assertEqual(phone_number,
            self.marionette.find_element(*dialer_object._calling_number_locator).text)

        # hang up before the person answers ;)
        dialer_object.hang_up(self)

