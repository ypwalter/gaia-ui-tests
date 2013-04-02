# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserNavigation(GaiaTestCase):

    _community_link_locator = ('css selector', '#community a')
    _community_history_section_locator = ('id', 'history')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_browser_back_button(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/450
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')

        browser.switch_to_content()
        self.verify_home_page()
        self.marionette.tap(self.marionette.find_element(*self._community_link_locator))

        self.verify_community_page()
        browser.switch_to_chrome()
        browser.tap_back_button()

        browser.switch_to_content()
        self.verify_home_page()
        browser.switch_to_chrome()
        browser.tap_forward_button()

        browser.switch_to_content()
        self.verify_community_page()

    def verify_home_page(self):
        self.wait_for_element_present(*self._community_link_locator)
        community_link = self.marionette.find_element(*self._community_link_locator)
        self.assertTrue(community_link.is_displayed, 'The community link was not visible at mozilla.html.')

    def verify_community_page(self):
        self.wait_for_element_present(*self._community_history_section_locator)
        history_section = self.marionette.find_element(*self._community_history_section_locator)
        self.assertTrue(history_section.is_displayed, 'The history section was not visible at mozilla_community.html.')
