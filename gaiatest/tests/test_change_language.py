# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestChangeLanguage(GaiaTestCase):

    # Language settings locators
    _settings_header_text_locator = ('css selector', '#root > header > h1')
    _language_settings_locator = ('id', 'menuItem-languageAndRegion')
    _select_language_locator = ('css selector', 'li:nth-child(1) .fake-select')
    _option_language_locator = ('css selector', '.fake-select>select>option[value="pt-BR"]')
    _back_button_locator = ('css selector', '.icon.icon-back')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # Launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_change_language_settings(self):
        before_language_change = self.marionette.find_element(*self._settings_header_text_locator).text

        # Navigate to Language settings
        self.wait_for_element_present(*self._language_settings_locator)
        language_item = self.marionette.find_element(*self._language_settings_locator)

        # Select Language
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [language_item])
        self.marionette.tap(language_item)

        self.wait_for_element_present(*self._select_language_locator)

        select_language_option = self.marionette.find_element(*self._option_language_locator)

        select_language_option.click()

        # Go back to Settings menu
        go_back = self.marionette.find_element(*self._back_button_locator)
        go_back.click()

        after_language_change = self.marionette.find_element(*self._settings_header_text_locator).text

        # Verify that language has changed
        self.assertNotEqual(before_language_change, after_language_change)

    def tearDown(self):

        # Change language back to English
        self.data_layer.set_setting("language.current", "en-US")

        GaiaTestCase.tearDown(self)
