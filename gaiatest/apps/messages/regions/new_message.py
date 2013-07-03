# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class NewMessage(Base):

    _recipients_list_locator = ('id', 'messages-recipients-list')
    _receiver_input_locator = ('css selector', '#messages-recipients-list span.recipient')
    _message_field_locator = ('id', 'messages-input')
    _send_message_button_locator = ('id', 'messages-send-button')
    _message_sending_spinner_locator = ('css selector', "img[src='style/images/spinningwheel_small_animation.gif']")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._recipients_list_locator)

    def type_phone_number(self, value):
        contact_field = self.marionette.find_element(*self._receiver_input_locator)
        contact_field.send_keys(value)

    def type_message(self, value):
        # change the focus to the message field to enable the send button
        message_field = self.marionette.find_element(*self._message_field_locator)
        message_field.tap()
        message_field.send_keys(value)

    def tap_send(self):
        self.marionette.find_element(*self._send_message_button_locator).tap()
        self.wait_for_element_not_present(*self._message_sending_spinner_locator, timeout=120)
        from gaiatest.apps.messages.regions.message_thread import MessageThread
        return MessageThread(self.marionette)
