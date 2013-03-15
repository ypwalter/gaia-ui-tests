# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestCostControlReset(GaiaTestCase):

    _welcome_title_locator = ('css selector', 'h1[data-l10n-id="fte-welcome-title"]')
    _usage_app_title_locator = ('css selector', 'h1[data-l10n-id="usage"]')

    _mobile_data_tracking_locator = ('id', 'mobileCheck')
    _wifi_data_tracking_locator = ('id', 'wifiCheck')
    _wifi_overview_data_locator = ('id', 'wifiOverview')

    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")

    _settings_title_locator = ('css selector', 'section#settings-view h1')
    _settings_button_locator = ('css selector', 'button.settings-button')
    _settings_iframe_locator = ('id', "settings-view-placeholder")
    _reset_button_locator = ('id', 'reset-data-usage')
    _reset_confirm_locator = ('css selector', 'section#reset-confirmation-dialog button.danger')
    _done_button_locator = ('css selector', 'section#settings-view button#close-settings')

    _wifi_data_locator = ('css selector', 'p#wifi-data-usage span.usage')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # launch the Gallery app
        self.app = self.apps.launch('Usage')

    def test_cost_control_ftu(self):
        # close fte from javascript.
        self.marionette.execute_script("return window.wrappedJSObject.ConfigManager.setOption({ fte: false });")
        self.marionette.refresh()

        # wait for usage app main screen to come out
        self.wait_for_element_displayed('id', 'datausage-tab')

        # make sure wifi tracking is on and mobile data tracking is off
        mobileswitch = self.marionette.find_element(*self._mobile_data_tracking_locator)
        wifiswitch = self.marionette.find_element(*self._wifi_data_tracking_locator)
        if mobileswitch.is_selected():
            self.marionette.tap(mobileswitch)
        if not wifiswitch.is_selected():
            self.marionette.tap(wifiswitch)

        # make sure the wifi is not 0 kb now. otherwise, open browser to get some data downloaded
        if self.marionette.find_element(*self._wifi_overview_data_locator).text == u'0.00 B':
            # open browser and do something
            self.apps.launch('Browser')
            self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))

            # go to a website
            awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
            awesome_bar.send_keys('http://mozqa.com/data/firefox/layout/mozilla.html')

            url_button = self.marionette.find_element(*self._url_button_locator)
            self.marionette.tap(url_button)

            # wait for it to load website
            try:
                self.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=20)
            except:
                pass

            self.apps.launch('Usage')
            self.wait_for_element_displayed(*self._usage_app_title_locator)

        # disable wifi before reset data, wait for wifi to be closed, and switch back to self.app
        self.data_layer.disable_wifi()
        time.sleep(1)
        self.marionette.switch_to_frame(self.marionette.find_element('css selector', 'iframe[data-url="app://costcontrol.gaiamobile.org/index.html#datausage-tab"]'))

        # go to settings section
        settings = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(settings)

        # go into iframe of usage app settings
        settings_iframe = self.marionette.find_element(*self._settings_iframe_locator)
        self.marionette.switch_to_frame(settings_iframe)

        # reset data
        self.wait_for_element_displayed(*self._settings_title_locator)
        reset = self.marionette.find_element(*self._reset_button_locator)
        self.marionette.tap(reset)
        confirm = self.marionette.find_element(*self._reset_confirm_locator)
        self.marionette.tap(confirm)
        done = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done)

        # waiting for usage to be refreshed and checking for usage
        time.sleep(2)
        self.assertTrue(self.marionette.find_element(*self._wifi_data_locator).text == u'0.00 B')

    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).get_attribute('class') == 'loading'
