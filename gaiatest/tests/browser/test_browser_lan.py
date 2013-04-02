# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserLAN(GaiaTestCase):

    _page_title_locator = ("id", "page-title")

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_browser_lan(self):
        # https://moztrap.mozilla.org/manage/case/1327/
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')

        browser.switch_to_content()

        self.wait_for_element_present(*self._page_title_locator)
        heading = self.marionette.find_element(*self._page_title_locator)
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

    def tearDown(self):
        if self.wifi:
            self.data_layer.disable_wifi()
        GaiaTestCase.tearDown(self)
