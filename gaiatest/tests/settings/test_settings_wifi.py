# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

class TestSettingsWifi(GaiaTestCase):

    # Wifi Settings locators
    _wifi_menu_item_locator = ('id', 'menuItem-wifi')
    _wifi_enabled_label_locator = ('css selector', '#wifi-enabled label')
    _wifi_enabled_checkbox_locator = ('css selector', '#wifi-enabled input')
    _available_networks_locator = ('css selector', '#wifi-availableNetworks li[class^="wifi-signal"]')
    _connected_message_locator = ('css selector', '#wifi-availableNetworks li.active small')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_connect_to_wifi_via_settings_app(self):
        """ Connect to wifi via the Settings app

        https://github.com/mozilla/gaia-ui-tests/issues/342

        """

        # navigate to wifi settings
        self.wait_for_element_present(*self._wifi_menu_item_locator)
        wifi_menu_item = self.marionette.find_element(*self._wifi_menu_item_locator)
        self.marionette.tap(wifi_menu_item)

        # enable wifi
        self.wait_for_element_present(*self._wifi_enabled_checkbox_locator)
        enabled_checkbox = self.marionette.find_element(*self._wifi_enabled_checkbox_locator)
        self.assertIsNone(enabled_checkbox.get_attribute('checked'))
        # we have to tap on the label rather than the input
        enabled_label = self.marionette.find_element(*self._wifi_enabled_label_locator)
        self.marionette.tap(enabled_label)

        # Wait for some networks to be found
        self.wait_for_condition(lambda m: len(m.find_elements(*self._available_networks_locator)) > 0,
            message="No networks listed on screen")

        # TODO This will only work on Mozilla Guest or unsecure network
        this_network_locator = ('xpath', "//li/a[text()='%s']" % self.testvars['wifi']['ssid'])
        wifi_network = self.marionette.find_element(*this_network_locator)
        self.marionette.tap(wifi_network)

        self.wait_for_condition(
            lambda m: self.marionette.find_element(*self._connected_message_locator).text == "Connected")

        # verify that wifi is now on
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via Settings app")
