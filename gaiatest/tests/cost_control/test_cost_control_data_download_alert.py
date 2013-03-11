# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCostControlDataDownloadAlert(GaiaTestCase):

    _welcome_title_locator = ('css selector', 'h1[data-l10n-id="fte-welcome-title"]')
    _next_button_locator = ('css selector', 'span[data-l10n-id="next"]')
    _ftu_usage_locator = ('css selector', 'section#non-vivo-step-2 span.tag')
    _ftu_data_alert_switch_locator = ('css selector', 'section#non-vivo-step-2 input')
    _capacity_button_locator = ('css selector', 'section#data-limit-dialog form button')
    _size_input_locator = ('css selector', 'section#data-limit-dialog form input')
    _usage_done_button_locator = ('css selector', '#data-usage-done-button')
    _go_button_locator = ('css selector', 'section#non-vivo-step-2 button.recommend')

    _settings_button_locator = ('css selector', 'button.settings-button')
    _data_alert_switch_locator = ('css selector', 'input[data-option="dataLimit"]')
    _data_limit_locator = ('css selector', 'button[data-widget-type="data-limit"] span')

    _url = 'http://tw.yahoo.com/'
    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    _cost_control_widget_locator = ('css selector', 'iframe[data-frame-origin="app://costcontrol.gaiamobile.org"]')
    _data_usage_view_locator = ('css selector', '#datausage-limit-view')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # launch the Gallery app
        self.app = self.apps.launch('Usage')

    def test_download_alert(self):
        self.wait_for_element_displayed(*self._settings_button_locator)
        self.wait_for_element_displayed(self._welcome_title_locator)

        # if welcome screen displayed for Usage/Cost Control app, then go through it, else do something else
        if self.marionette.find_element(*self._welcome_title_locator).is_displayed:
            # click 'next'
            nt = self.marionette.find_element(*self._next_button_locator)
            self.marionette.tap(nt)

            # click 'next'
            nt = self.marionette.find_element(*self._next_button_locator)
            self.marionette.tap(nt)

            # enable the switch for data alert
            switch = self.marionette.find_elements(*self._ftu_data_alert_switch_locator)
            self.marionette.tap(switch)

            # change the data alert from whatever the setting is to 0.1MB
            usage = self.marionette.find_element()
            self.marionette.tap(usage)
            capacity = self.marionette.find_element(*self._capacity_button_locator)
            if capacity == 'GB':
                self.marionette.tap(capacity)
            size = self.marionette.find_element(*self._size_input_locator)
            size.clear()
            size.send_keys('0.1')
            done = self.marionette.find_element(*self._usage_done_button_locator)
            self.marionette.tap(done)

            go = self.marionette.find_element(*self._go_button_locator)
            self.marionette.tap(go)

        # if not first time launching cost control app, doing the following
        else:
            # go into settings for enabling it
            settings = self.marionette.find_element(*self._settings_button_locator)
            self.marionette.tap(settings)

            # enable data use alert if not enabled
            switch = self.marionette.find_element(*self._data_alert_switch_locator)
            if not switch.is_selected():
                self.marionette.tap(switch)

            # make sure the data alert is 0.1MB, or we would set it to 0.1MB
            self.marionette.find_element(self._capacity_button_locator).click()
            capacity = self.marionette.find_element(*self._capacity_button_locator)
            if capacity == 'GB':
                self.marionette.tap(capacity)
            size = self.marionette.find_element(*self._size_input_locator)
            size.clear()
            size.send_keys('0.1')
            done = self.marionette.find_element(*self._usage_done_button_locator)
            self.marionette.tap(done)

        # go to browser and go beyond the usage
        browser = self.apps.launch('Browser')
        self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))
        self.marionette.switch_to_frame(browser)
        for i in range(3):
            awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
            awesome_bar.send_keys(url)

            url_button = self.marionette.find_element(*self._url_button_locator)
            self.marionette.tap(url_button)

            # Wait for throbber
            self.wait_for_element_displayed(*self._throbber_locator)

            # Bump up the timeout due to slower cell data speeds
            self.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=120)

        # get the notification bar
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")

        # switch to cost control widget
        usage_iframe = self.marionette.find_element(*self._cost_control_widget_locator)
        self.marionette.switch_to_frame(usage_iframe)

        # make sure the color changed
        bar = self.marionette.find_element(*self._data_usage_view_locator)
        self.assertTrue('reached-limit' in bar.get_attribute('class'))

