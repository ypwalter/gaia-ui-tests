# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.tests.dialer import dialer_object


class TestDialer(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the app
        self.app = self.apps.launch('Phone')

    def test_dialer_make_call(self):
        # https://moztrap.mozilla.org/manage/case/1298/

        self.assertTrue(self.testvars, 'Test variables file not provided')
        self.assertTrue('remote_phone_number' in self.testvars,
                        'No remote phone number present in test variables file')
        self._test_phone_number = self.testvars['remote_phone_number']
        self.assertTrue(self._test_phone_number,
                        'Remote phone number in test variables file is empty')

        dialer_object.wait_for_ready_to_dial(self)

        dialer_object.dial_number(self, self._test_phone_number)

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(
            *dialer_object._phone_number_view_locator)

        self.assertEqual(
            phone_view.get_attribute('value'), self._test_phone_number)

        # Now press call!
        dialer_object.place_call(self)

        # Check the number displayed is the one we dialed
        self.assertEqual(self._test_phone_number,
            self.marionette.find_element(*dialer_object._calling_number_locator).text)

        # hang up before the person answers ;)
        dialer_object.hang_up(self)

