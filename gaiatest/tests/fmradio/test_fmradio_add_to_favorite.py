# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestFMRadioAddToFavorite(GaiaTestCase):

    _warning_page_locator = ('id', 'antenna-warining')
    _frequency_display_locator = ('id', 'frequency')
    _favorite_button_locator = ('id', 'bookmark-button')
    _power_button_locator = ('id', 'power-switch')
    _favorite_list_locator = ('css selector', "div[class='fav-list-frequency']")
    _favorite_remove_locator = ('css selector', "div[class='fav-list-remove-button']")

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.lockscreen.unlock()

        # launch the FM Radio app
        self.app = self.apps.launch('FM Radio')

    def test_add_to_favorite(self):
        """ Add a frequency to favorite list

        https://moztrap.mozilla.org/manage/case/1923/

        """
        # check the headphone is plugged-in or not
        self.wait_for_element_not_displayed(*self._warning_page_locator)

        # wait for the radio start-up
        self.wait_for_condition(lambda m: m.find_element(*self._power_button_locator).get_attribute('data-enabled') == 'true')

        # save the initial count of favorite stations
        initial_favorite_count = len(self.marionette.find_elements(*self._favorite_list_locator))

        # save the current frequency
        current_frequency = self.marionette.find_element(*self._frequency_display_locator).text

        # add the current frequency to favorite list
        self.wait_for_element_displayed(*self._favorite_button_locator)
        self.marionette.find_element(*self._favorite_button_locator).click()

        # verify the change of favorite list
        favorite_list = self.marionette.find_elements(*self._favorite_list_locator)
        new_favorite_count = len(favorite_list)
        self.assertEqual(initial_favorite_count, new_favorite_count - 1)

        # verify the favorite frequency is equal to the current frequency
        favorite_frequency = favorite_list[0].text
        self.assertEqual(current_frequency, favorite_frequency)

    def tearDown(self):
        # remove the station from favorite list
        self.wait_for_element_displayed(*self._favorite_remove_locator)
        self.marionette.find_element(*self._favorite_remove_locator).click()

        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
