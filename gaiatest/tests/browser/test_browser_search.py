# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserSearch(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_browser_search(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/451
        browser = Browser(self.marionette)
        browser.launch()

        search_text = 'Mozilla Web QA'

        browser.go_to_url(search_text)

        browser.switch_to_content()
        self.assertEqual('Bing : %s' % search_text, browser.page_title)
        self.assertEqual(search_text, browser.bing_search_input)

    def tearDown(self):
        if self.wifi:
            self.data_layer.disable_wifi()
        GaiaTestCase.tearDown(self)
