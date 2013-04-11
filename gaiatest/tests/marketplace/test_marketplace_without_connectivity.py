# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestMarketplaceWithoutConnectivity(GaiaTestCase):

    expected_error_title = u'Network connection unavailable'
    expected_error_message = u'Marketplace requires a network connection. Try connecting to a Wi-Fi or mobile data network.'

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.data_layer.disable_cell_data()
        self.data_layer.disable_cell_roaming()
        self.data_layer.disable_wifi()

    def test_marketplace_without_connectivity(self):
        marketplace = Marketplace(self.marionette)
        marketplace.launch()

        self.marionette.switch_to_frame()

        self.assertEqual(marketplace.error_title_text, self.expected_error_title)
        self.assertEqual(marketplace.error_message_text, self.expected_error_message)
