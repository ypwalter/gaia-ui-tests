# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestEverythingMe(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _app_icon_locator = ('css selector', "div.evme-apps li.cloud")

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_landing_locator = ('id', 'landing-page')

    # Linkedin app locator
    _linkedIn_iframe_locator = ('css selector', "iframe[data-url*='touch.www.linkedin.com']")
    _linkedIn_title_locator = ('tag name', 'title')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        self.lockscreen.unlock()

    def test_launch_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/69

        # I have requested a HTML enhancement for more reliable testing:
        # https://bugzilla.mozilla.org/show_bug.cgi?id=845828

        # swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

        # check for the available shortcut categories
        self.wait_for_element_present(*self._shortcut_items_locator)

        # We can't locate by name because they are stored as images
        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')

        # Instead, we tap on the first category of shortcuts
        self.marionette.tap(shortcuts[0])

        self.wait_for_element_displayed(*self._app_icon_locator)

        # Due to everythingme HTML we cannot locate by the text...
        app_icons = self.marionette.find_elements(*self._app_icon_locator)
        # ... so we'll just get the first one.
        self.marionette.tap(app_icons[0])

        # Switch to top level frame then we'll look for the LinkedIn app
        self.marionette.switch_to_frame()

        # Find the frame and switch to it
        li_iframe = self.wait_for_element_present(*self._linkedIn_iframe_locator)
        self.marionette.switch_to_frame(li_iframe)

        li_title = self.marionette.find_element(*self._linkedIn_title_locator)
        self.assertIn("LinkedIn", li_title.text)

    def tearDown(self):
        # this will take us back to everything.me Social page, from whence cleanUp can return to the home page
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        GaiaTestCase.tearDown(self)
