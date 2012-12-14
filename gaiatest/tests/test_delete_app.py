# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

MANIFEST = 'http://mozqa.com/data/webapps/mozqa.com/manifest.webapp'
APP_NAME = 'Mozilla QA WebRT Tester'
TITLE = 'Index of /data'

class TestDeletApp(GaiaTestCase):
    _yes_button_locator = ('id', 'app-install-install-button')
    # locator for li.icon, because click on label doesn't work.
    _icon_locator = ('css selector', 'li.icon[aria-label="%s"]' % APP_NAME)


    def setUp(self):
        GaiaTestCase.setUp(self)

        self.homescreen = self.apps.launch('Homescreen')

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
        self._touch_home_button()

        # go the first page
        self._go_to_next_page()
        self.marionette.switch_to_frame()

        app_icon = self.marionette.find_element(*self._icon_locator)

        self.marionette.long_press(app_icon, 10000)
        self.marionette.switch_to_frame()

    def _touch_home_button(self):
        self.marionette.execute_script("return window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def tearDown(self):
        self.apps.kill_all()
        self.apps.uninstall(APP_NAME)
        GaiaTestCase.tearDown(self)
