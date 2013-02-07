# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

class TestEverythingMeInstallApp(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _facebook_icon_locator = ('xpath', "//div/b[text()='Facebook']")

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_facebook_icon_locator = ('css selector', 'li.icon[aria-label="Facebook"]')

    # Modal dialog locators
    _modal_dialog_message_locator = ('id','modal-dialog-confirm-message')
    _modal_dialog_ok_locator = ('id', 'modal-dialog-confirm-ok')


    def setUp(self):

        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        self.lockscreen.unlock()

    def test_installing_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/67

        # swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

        # check for the available shortcut categories
        self.wait_for_element_present(*self._shortcut_items_locator)

        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')

        # Tap on the first category of shortcuts
        self.marionette.tap(shortcuts[0])

        self.wait_for_element_displayed(*self._facebook_icon_locator)

        fb_icon = self.marionette.find_element(*self._facebook_icon_locator)
        self.marionette.long_press(fb_icon)

        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self._modal_dialog_ok_locator) # wait for the modal dialog

        modal_dialog_message = self.marionette.find_element(*self._modal_dialog_message_locator).text
        self.assertIn("Facebook", modal_dialog_message)

        modal_dialog_ok_button  = self.marionette.find_element(*self._modal_dialog_ok_locator)
        self.marionette.tap(modal_dialog_ok_button)

        # return to home screen
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        self.marionette.switch_to_frame(hs_frame)

        while not self.is_element_displayed(*self._homescreen_facebook_icon_locator):
            self._go_to_next_page()

        self.assertTrue(self.marionette.find_element(*self._homescreen_facebook_icon_locator).is_displayed())

    def tearDown(self):
        self.data_layer.delete_bookmark("Facebook")

        GaiaTestCase.tearDown(self)

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
