# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Browser(Base):

    name = "Browser"

    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")

    def launch(self):
        Base.launch(self)
        self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))

    def go_to_url(self, url):
        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.clear()
        awesome_bar.send_keys(url)

        self.tap_go_button()
        self.wait_for_throbber_not_visible()

    def switch_to_content(self):
        web_frame = self.marionette.find_element(*self._browser_frame_locator)
        self.marionette.switch_to_frame(web_frame)

    def switch_to_chrome(self):
        Base.launch(self)

    def tap_go_button(self):
        self.marionette.tap(self.marionette.find_element(*self._url_button_locator))

    def wait_for_throbber_not_visible(self):
        # TODO see if we can reduce this timeout in the future. >10 seconds is poor UX
        self.wait_for_condition(lambda m: not self.is_throbber_visible, timeout=20)

    @property
    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).get_attribute('class') == 'loading'
