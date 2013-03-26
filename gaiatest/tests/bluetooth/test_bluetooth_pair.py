# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestBluetoothPair(GaiaTestCase):

    _bluetooth_settings_locator = ('id', 'menuItem-bluetooth')
    _bluetooth_checkbox_locator = ('css selector', '#bluetooth-status input')
    _bluetooth_label_locator = ('css selector', '#bluetooth-status label')
    _device_list_locator = ('xpath', '//li[a="%s"]')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # turn on bluetooth
        self.data_layer.set_setting('bluetooth.enabled', True)

        # launch the settings app
        self.app = self.apps.launch('settings')

    def test_bluetooth_pair(self):

        # navigate to bluetooth settings
        self.wait_for_element_displayed(*self._bluetooth_settings_locator)
        bluetooth_menu_item = self.marionette.find_element(*self._bluetooth_settings_locator)
        self.marionette.tap(bluetooth_menu_item)

        # make sure bluetooth is on
        self.wait_for_element_present(*self._bluetooth_checkbox_locator)
        checkbox = self.marionette.find_element(*self._bluetooth_checkbox_locator)
        self.wait_for_condition(lambda m: checkbox.get_attribute('checked') == 'true')
        self.assertTrue(self.data_layer.get_setting('bluetooth.enabled'))

        # unpair all bluetooth devices if possible
        try:
            self.wait_for_element_displayed('id', 'bluetooth-paired-devices')
            paired_device = self.marionette.find_elements("css selector", "#bluetooth-paired-devices li")
            while len(paired_device) > 0:
                self.marionette.tap(paired_device[0])
                self.wait_for_element_displayed('id', 'unpair-option')
                unpair = self.marionette.find_element('id', 'unpair-option')
                self.marionette.tap(unpair)
                self.switch_to_frame()
                ok = self.marionette.find_element('id', 'modal-dialog-confirm-ok')
                self.marionette.tap(ok)
                self.marionette.wait_for_element_not_present('id', 'unpair-option')
                self.switch_to_frame(self.app.frame)
        except:
            pass

        # select the chosen devices to connect
        self.wait_for_element_displayed(self._device_list_locator[0], self._device_list_locator[1] % self.testvars['bluetooth']['device'])
        device = self.marionette.find_element(self._device_list_locator[0], self._device_list_locator[1] % self.testvars['bluetooth']['device'])
        self.marionette.tap(device)

        # check bluetooth device is connected
        self.wait_for_element_displayed('id', 'bluetooth-paired-devices')
        paired_device = self.marionette.find_elements("css selector", "#bluetooth-paired-devices a")
        self.assertEqual(len(paired_device), 1)
        self.assertEqual(paired_device[0].text, self.testvars['bluetooth']['device'])

    def tearDown(self):
        # Disable Bluetooth
        self.data_layer.set_setting('bluetooth.enabled', False)

        GaiaTestCase.tearDown(self)
