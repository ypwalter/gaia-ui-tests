# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestFMRadioFindStations(GaiaTestCase):

    _warning_page_locator = ('id', 'antenna-warning')
    _frequency_display_locator = ('id', 'frequency')
    _power_button_locator = ('id', 'power-switch')
    _next_button_locator = ('id', 'frequency-op-seekup')
    _prev_button_locator = ('id', 'frequency-op-seekdown')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.lockscreen.unlock()

        # launch the FM Radio app
        self.app = self.apps.launch('FM Radio')

    def test_find_next_station(self):
        """ Find next station

        https://moztrap.mozilla.org/manage/case/1928/

        """
        # check the headphone is plugged-in or not
        self.wait_for_element_not_displayed(*self._warning_page_locator)

        # wait for the radio start-up
        self.wait_for_condition(lambda m: m.find_element(*self._power_button_locator).get_attribute('data-enabled') == 'true')

        # save the current frequency
        current_frequency = self.marionette.find_element(*self._frequency_display_locator).text

        # search next station
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_condition(lambda m: m.find_element(*self._frequency_display_locator).text != current_frequency)

        # check the chagne of the frequency
        next_frequency = self.marionette.find_element(*self._frequency_display_locator).text
        self.assertNotEqual(current_frequency, next_frequency)

    def test_find_prev_station(self):
        """ Find previous station

        https://moztrap.mozilla.org/manage/case/1929/

        """
        # check the headphone is plugged-in or not
        self.wait_for_element_not_displayed(*self._warning_page_locator)

        # wait for the radio start-up
        self.wait_for_condition(lambda m: m.find_element(*self._power_button_locator).get_attribute('data-enabled') == 'true')

        # save the current frequency
        current_frequency = self.marionette.find_element(*self._frequency_display_locator).text

        # search next station
        self.marionette.find_element(*self._prev_button_locator).click()
        self.wait_for_condition(lambda m: m.find_element(*self._frequency_display_locator).text != current_frequency)

        # check the chagne of the frequency
        prev_frequency = self.marionette.find_element(*self._frequency_display_locator).text
        self.assertNotEqual(current_frequency, prev_frequency)

    def tearDown(self):
        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
