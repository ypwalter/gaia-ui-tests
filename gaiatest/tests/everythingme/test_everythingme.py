# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestEverythingMe(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _app_icon_locator = ('css selector', 'div.evme-apps li.cloud')
    _social_category_locator = ('xpath', "//li[@data-query='Social']")

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')
    _homescreen_landing_locator = ('id', 'landing-page')

    # Facebook app locator
    _facebook_iframe_locator = ('css selector', "iframe[data-url*='http://touch.facebook.com/']")
    _facebook_app_locator = ('xpath', "//li[@data-name='Facebook']")
    _facebook_title_locator = ('tag name', 'title')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_launch_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/69

        # Swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

        # Check for the available application shortcut categories
        self.wait_for_element_present(*self._shortcut_items_locator)

        # Check that there are shortcut application categories available
        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')

        # Tap on the 'Social' category
        social = self.marionette.find_element(*self._social_category_locator)
        self.marionette.tap(social)

        self.wait_for_element_displayed(*self._app_icon_locator)

        # Tap the available Facebook application shortcut
        app = self.marionette.find_element(*self._facebook_app_locator)
        self.marionette.tap(app)

        # Switch to top level frame then look for the Facebook app
        self.marionette.switch_to_frame()

        # Find the frame and switch to it
        app_iframe = self.wait_for_element_present(*self._facebook_iframe_locator)
        self.marionette.switch_to_frame(app_iframe)

        app_title = self.marionette.find_element(*self._facebook_title_locator)
        self.assertIn("Facebook", app_title.text)

    def tearDown(self):
        # This will take us back to Everything.Me 'Social' category, from whence cleanUp can return to the home page
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        GaiaTestCase.tearDown(self)
