# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestSearchMarketplacePaidApp(GaiaTestCase):

    MARKETPLACE_DEV_NAME = 'Marketplace Dev'
    MARKETPLACE_DEV_MANIFEST = 'https://marketplace-dev.allizom.org/manifest.webapp'

    MARKETPLACE_DEV_INSTALLED = False

    # System app confirmation button to confirm installing an app
    _yes_button_locator = ('id', 'app-install-install-button')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace_dev()

    def test_search_paid_app(self):
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()

        results = marketplace.search('')

        # validate the first result is the official lanyrd mobile app
        self.assertGreater(len(results.search_results), 0, 'No results found.')

        filter = results.tap_filter()
        filter.by_price('paid')
        results = filter.tap_apply()

        self.assertGreater(len(results.search_results), 0, 'No results found.')

        [self.assertTrue(re.match('^\$\d+\.\d{2}', result.price))
         for result in results.search_results]

    def install_marketplace_dev(self):
        # install the marketplace dev app
        self.marionette.execute_script('navigator.mozApps.install("%s")' % self.MARKETPLACE_DEV_MANIFEST)

        # TODO add this to the system app object when we have one
        self.wait_for_element_displayed(*self._yes_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._yes_button_locator))
        self.wait_for_element_not_displayed(*self._yes_button_locator)
        self.MARKETPLACE_DEV_INSTALLED = True

    def tearDown(self):

        if self.MARKETPLACE_DEV_INSTALLED:
            self.apps.uninstall(self.MARKETPLACE_DEV_NAME)

        GaiaTestCase.tearDown(self)
