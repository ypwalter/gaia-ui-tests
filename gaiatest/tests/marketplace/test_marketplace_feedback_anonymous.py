# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace
import time

class TestMarketplaceFeedback(GaiaTestCase):
    MARKETPLACE_DEV_NAME = 'Marketplace Dev'
    cmp_message = u'Feedback submitted. Thanks!'

    _settings_button_locator = ('css selector', 'a.header-button.settings')
    _feedback_tab_locator = ('css selector', 'a[href="/feedback"]')
    _feedback_textarea_locator = ('name', 'feedback')
    _submit_button_locator = ('css selector', 'button[type="submit"]')
    _notification_locator = ('id', 'notification')
    _notification_content_locator = ('id', 'notification-content')
    
    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace()

    def test_marketplace_feedback_anonymous(self):
        self.marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        self.marketplace.launch()
        self.marionette.switch_to_frame()
        self.marketplace.switch_to_marketplace_frame()

        self.wait_for_element_displayed(*self._settings_button_locator)
        self.marionette.find_element(*self._settings_button_locator).tap()
        self.marionette.find_element(*self._feedback_tab_locator).tap()

        feedback = self.marionette.find_element(*self._feedback_textarea_locator)
        feedback.clear()
        feedback.send_keys('This is a test comment.')
        self.marionette.execute_script('document.getElementsByName("feedback")[0].blur();')

        self.wait_for_element_displayed(*self._submit_button_locator)
        self.marionette.find_element(*self._submit_button_locator).tap()

        self.wait_for_element_displayed(*self._notification_locator)
        message = self.marionette.find_element(*self._notification_content_locator)
        message_content = message.get_attribute('innerHTML')

        self.assertEqual(message_content, self.cmp_message)
