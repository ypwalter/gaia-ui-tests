# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestFMRadioRemoveFromFavorite(GaiaTestCase):

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

    def test_remove_from_favorite(self):
        """ Remove a station from favorite list

        https://moztrap.mozilla.org/manage/case/1926/

        """
        # check the headphone is plugged-in or not
        self.wait_for_element_not_displayed(*self._warning_page_locator)

        # wait for the radio start-up
        self.wait_for_condition(lambda m: m.find_element(*self._power_button_locator).get_attribute('data-enabled') == 'true')

        # save the initial count of favorite stations
        initial_favorite_count = len(self.marionette.find_elements(*self._favorite_list_locator))

        # add the current frequency to favorite list
        self.wait_for_element_displayed(*self._favorite_button_locator)
        self.marionette.find_element(*self._favorite_button_locator).click()

        # verify the change of favorite list after add
        after_add_favorite_count = len(self.marionette.find_elements(*self._favorite_list_locator))
        self.assertEqual(initial_favorite_count, after_add_favorite_count - 1)

        # remove the station from favorite list
        self.wait_for_element_displayed(*self._favorite_remove_locator)
        self.marionette.find_element(*self._favorite_remove_locator).click()

        # verify the chage of favorite after remove
        self.wait_for_element_not_displayed(*self._favorite_remove_locator)
        after_remove_favorite_count = len(self.marionette.find_elements(*self._favorite_list_locator))
        self.assertEqual(after_add_favorite_count - 1, after_remove_favorite_count)

    def tearDown(self):
        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
