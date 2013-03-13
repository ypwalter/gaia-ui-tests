# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestEverythingMeInstallApp(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _apps_icon_locator = ('css selector', 'div.evme-apps li.cloud')

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_icon_locator = ('css selector', 'li.icon[aria-label="%s"]')

    # Modal dialog locators
    _modal_dialog_message_locator = ('id', 'modal-dialog-confirm-message')
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

        self.wait_for_element_displayed(*self._apps_icon_locator)

        first_app_icon = self.marionette.find_element(*self._apps_icon_locator)
        self.first_app_name = first_app_icon.text
        self.marionette.long_press(first_app_icon)

        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self._modal_dialog_ok_locator)  # wait for the modal dialog

        modal_dialog_message = self.marionette.find_element(*self._modal_dialog_message_locator).text

        self.first_app_name = modal_dialog_message[
            modal_dialog_message.find('Add') + 3:
            modal_dialog_message.find('to Home Screen?')
        ].strip()  # TODO remove hack after Bug 845828 lands in V1-train

        modal_dialog_ok_button = self.marionette.find_element(*self._modal_dialog_ok_locator)
        self.marionette.tap(modal_dialog_ok_button)

        # return to home screen
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        self.marionette.switch_to_frame(hs_frame)

        # check whether app is installed
        app_installed = False
        while self._homescreen_has_more_pages:
            if self.is_element_displayed(self._homescreen_icon_locator[0], self._homescreen_icon_locator[1] % self.first_app_name):
                app_installed = True
                break
            self._go_to_next_page()

        self.assertTrue(app_installed, 'The app %s was not found to be installed on the home screen.' % self.first_app_name)

    def tearDown(self):
        self.delete_bookmark(self.first_app_name)

        GaiaTestCase.tearDown(self)

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    @property
    def _homescreen_has_more_pages(self):
        # the naming of this could be more concise when it's in an app object!
        return self.marionette.execute_script("""
        var pageHelper = window.wrappedJSObject.GridManager.pageHelper;
        return pageHelper.getCurrentPageNumber() < (pageHelper.getTotalPagesNumber() - 1);""")

    def delete_bookmark(self, bookmark_name):
        self.marionette.execute_script("""
                                          name = arguments[0];
                                          let apps = window.wrappedJSObject.GridManager.getApps();
                                          apps.forEach (function(aApp) {
                                            if (aApp.isBookmark) {
                                              if (aApp.manifest.name == name) {
                                                console.log('uninstalling app with name ' + aApp.manifest.name);
                                                aApp.uninstall();
                                              };
                                            };
                                          });
                                        """, script_args=[bookmark_name])
