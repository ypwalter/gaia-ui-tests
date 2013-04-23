# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.keyboard.app import Keyboard

class TestKeyboard(GaiaTestCase):

    # UI Tests app locators
    _test_message_title_locator = ('css selector', 'h1[data-l10n-id="messages"]')
    _new_message_icon_locator = ('id', 'icon-add')
    _text_input_locator = ('id', 'messages-recipient')

    _test_string = "aG1D2s3~!=@.#$^"
    _test_string2 = "aśZïd"
    _final_string = "aG1D2s3~!=@.#$ aśZïdÆ"

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Messages app
        self.app = self.apps.launch('Messages')

    def test_keyboard_basic(self):
        # initialize the keyboard app
        kbapp = Keyboard(self.marionette)

        # wait for app to load
        self.wait_for_element_displayed(*self._test_message_title_locator)

        # do a new message
        new_message = self.marionette.find_element(*self._new_message_icon_locator)
        self.marionette.tap(new_message)

        # tap the message composition area
        self.wait_for_element_displayed(*self._text_input_locator)
        message_composition = self.marionette.find_element(*self._text_input_locator)
        self.marionette.tap(message_composition)

        # send first string and delete last character
        kbapp.send(self._test_string)
        kbapp.tap_backspace()
        kbapp.tap_space()

        # send second string
        kbapp.send(self._test_string2.decode('UTF-8'))

        # select special character using extended character selector
        kbapp.choose_extended_character('A', 8)

        # go back to app frame and finish this
        self.marionette.switch_to_frame(self.app.frame)

        self.wait_for_element_displayed(*self._text_input_locator)
        output_text = self.marionette.find_element(*self._text_input_locator).get_attribute("value")

        self.assertEqual(self._final_string, output_text.encode('UTF-8'))
