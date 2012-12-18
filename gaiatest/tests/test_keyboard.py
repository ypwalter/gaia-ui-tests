# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase


class TestKeyboard(GaiaTestCase):

    # UI Tests app locators
    _test_keyboard_link_locator = ('link text', 'Keyboard test')
    _text_input_locator = ('css selector', "input[type='text']")

    # Keyboard app
    _keyboard_frame_locator = ('css selector','#keyboard-frame iframe')

    _test_string = "myhovercraftisfullofeels"

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the UI Tests app
        self.app = self.apps.launch('UI tests')

    def test_keyboard_basic(self):

        # wait for app to load
        self.wait_for_element_displayed(*self._test_keyboard_link_locator)

        # click/load the Keyboard test page
        self.marionette.find_element(*self._test_keyboard_link_locator).click()

        test_page_frame = self.marionette.find_element('id','test-iframe')
        self.marionette.switch_to_frame(test_page_frame)

        time.sleep(2)

        self.wait_for_element_displayed(*self._text_input_locator)
        self.marionette.find_element(*self._text_input_locator).click()

        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._keyboard_frame_locator)
        page = self.marionette.page_source
        self.marionette.switch_to_frame('keyboard')

        for char in self._test_string:
            key = self.marionette.find_element('xpath', "//button[span/span[text()='%s']]" % char)
            print key.text
            key.click()

        time.sleep(10)

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)