# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base


class Phone(Base):

    name = "Phone"

    _dialog_locator = ('id', 'confirmation-message')
    _dialog_title_locator = ('xpath', "//*[@id='confirmation-message']/section/h1")

    @property
    def keypad(self):
        from gaiatest.apps.phone.regions.keypad import Keypad
        return Keypad(self.marionette)

    @property
    def call_screen(self):
        from gaiatest.apps.phone.regions.call_screen import CallScreen
        return CallScreen(self.marionette)

    @property
    def confirmation_dialog_text(self):
        return self.marionette.find_element(*self._dialog_title_locator).text

    def wait_for_confirmation_dialog(self):
        self.wait_for_element_displayed(*self._dialog_locator)

