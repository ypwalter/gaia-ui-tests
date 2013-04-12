# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestSearchMarketplaceAndInstallApp(GaiaTestCase):

    APP_NAME = 'Lanyrd'
    APP_DEVELOPER = 'Lanyrd'
    APP_INSTALLED = False

    # Label identifier for all homescreen apps
    _app_icon_locator = ('xpath', "//li[@class='icon']//span[text()='%s']" % APP_NAME)
    _homescreen_iframe_locator = ('css selector', 'div.homescreen iframe')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_search_and_install_app(self):
        marketplace = Marketplace(self.marionette)
        marketplace.launch()

        print self.marionette.page_source

        marketplace.search(self.APP_NAME)

        # validate the first result is the official lanyrd mobile app
        self.assertGreater(len(marketplace.search_results), 0, 'No results found.')

        first_result = marketplace.search_results[0]

        self.assertEquals(first_result.name, self.APP_NAME, 'First app has the wrong name.')
        self.assertEquals(first_result.author, self.APP_DEVELOPER, 'First app has the wrong author.')

        # Find and click the install button to the install the web app
        self.assertEquals(first_result.install_button_text, 'Free', 'Incorrect button label.')

        first_result.tap_install_button()
        marketplace.confirm_installation()
        self.APP_INSTALLED = True

        # Check that the icon of the app is on the homescreen
        self.marionette.switch_to_frame()
        homescreen_frame = self.marionette.find_element(*self._homescreen_iframe_locator)
        self.marionette.switch_to_frame(homescreen_frame)
        self.assertTrue(marketplace.self.marionette.find_element(*self._app_icon_locator))

    def tearDown(self):

        if self.APP_INSTALLED:
            self.apps.uninstall(self.APP_NAME)

        GaiaTestCase.tearDown(self)
