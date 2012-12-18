# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

MANIFEST = 'http://mozqa.com/data/webapps/mozqa.com/manifest.webapp'
APP_NAME = 'Mozilla QA WebRT Tester'
TITLE = 'Index of /data'


class TestDeleteApp(GaiaTestCase):

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'iframe.homescreen')

    # locator for li.icon, because click on label doesn't work.
    _icon_locator = ('css selector', 'li.icon[aria-label="%s"]' % APP_NAME)
    _delete_app_locator = ('css selector', 'span.options')

    # App install popup
    _yes_button_locator = ('id', 'app-install-install-button')

    # Delete popup
    _confirm_delete_locator = ('id', 'confirm-dialog-confirm-button')


    def setUp(self):
        GaiaTestCase.setUp(self)

        self.homescreen = self.apps.launch('Homescreen')

        # Activate wifi
        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # install app
        self.marionette.switch_to_frame()
        self.marionette.execute_script(
            'navigator.mozApps.install("%s")' % MANIFEST)

        # click yes on the installation dialog and wait for icon displayed
        self.wait_for_element_displayed(*self._yes_button_locator)
        yes = self.marionette.find_element(*self._yes_button_locator)
        yes.click()
        self.marionette.switch_to_frame(self.homescreen.frame_id)
        self.wait_for_element_displayed(*self._icon_locator)

    def test_delete_app(self):

        #go to home screen
        self.marionette.switch_to_frame()
        self._touch_home_button()

        # go the first page
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        self._go_to_next_page()

        #check that the app is available
        app_icon = self.marionette.find_element(*self._icon_locator)
        self.assertTrue(app_icon.is_displayed())

        # go to edit mode.
        # TODO: activate edit mode using HOME button https://bugzilla.mozilla.org/show_bug.cgi?id=814425
        self._activate_edit_mode()

        # delete the app
        delete_button = app_icon.find_element(*self._delete_app_locator)
        delete_button.click()

        self.wait_for_element_displayed(*self._confirm_delete_locator)
        delete = self.marionette.find_element(*self._confirm_delete_locator)
        delete.click()

        self.wait_for_element_not_present(*self._icon_locator)

        # return to normal mode
        self.marionette.switch_to_frame()
        self._touch_home_button()

        #check that the app is no longer available
        with self.assertRaises(AssertionError):
            self.apps.launch(APP_NAME)

    def _touch_home_button(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def _activate_edit_mode(self):
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")

    def tearDown(self):
        self.apps.kill_all()
        GaiaTestCase.tearDown(self)
