# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class MessageThread(Base):

    _all_messages_locator = ('css selector', '#messages-container li.message')
    _received_message_content_locator = ('css selector', "#messages-container li.message.received")

    def wait_for_received_messages(self):
        self.wait_for_element_displayed(*self._received_message_content_locator)

    @property
    def received_messages(self):
        return [Message(self.marionette, message) for message in self.marionette.find_elements(*self._received_message_content_locator)]

    @property
    def all_messages(self):
        return [Message(self.marionette, message) for message in self.marionette.find_elements(*self._all_messages_locator)]


class Message(PageRegion):
    _text_locator = ('css selector', '.bubble > p')

    @property
    def text(self):
        return self.root_element.find_element(*self._text_locator).text

    @property
    def id(self):
        return self.root_element.get_attribute('id')
