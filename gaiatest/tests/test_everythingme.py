# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

class TestEverythingMe(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'iframe.homescreen')
    _homescreen_landing_locator = ('id', 'landing-page')

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.lockscreen.unlock()

        self.data_layer.disable_wifi()
        self.data_layer.enable_cell_data()

    def test_launch_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/69

        # start on the home-screen
        self._touch_home_button()

        # swipe to Everything.Me
        self._swipe_to_everything_me()

        # check for the available shortcut categories 
        self.wait_for_element_present(*self._shortcut_items_locator, timeout=180)

        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'no shortcut categories found')

        # click on the first category of shortcuts
        # Does not work?
        ### shortcuts[0].click()
        
        # wait and click on a shortcut in the category

        # verify launch
        # close and exit back to home
        self._touch_home_button()


    def _swipe_to_everything_me(self):

        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        landing_element = self.marionette.find_element(*self._homescreen_landing_locator)
        landing_element_x_centre = int(landing_element.size['width']/2)
        landing_element_y_centre = int(landing_element.size['height']/2)

        self.assertTrue(landing_element.is_displayed(), "Landing element not displayed after unlocking")
        self.marionette.flick(landing_element, landing_element_x_centre, landing_element_y_centre, 300, 0, 0)

    def _touch_home_button(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        self.data_layer.disable_cell_data()

        GaiaTestCase.tearDown(self)
