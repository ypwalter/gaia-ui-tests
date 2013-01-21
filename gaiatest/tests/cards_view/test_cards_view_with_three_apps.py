# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from marionette.errors import NoSuchElementException
import time

class TestCardsViewThreeApps(GaiaTestCase):

    _first_app = "Clock"
    _second_app = "Gallery"
    _third_app = "Calendar"

    # Home/Cards view locators
    _cards_view_locator = ('id', 'cards-view')
    # Check that the origin contains the current app name, origin is in the format:
    # app://clock.gaiamobile.org
    _app_card_locator = ('css selector', '#cards-view li.card[data-origin*="%s"]')
    _close_button_locator = ('css selector', '#cards-view li.card[data-origin*="%s"] .close-card')

    _homescreen_frame_locator = ('id', 'lockscreen')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the test apps
        self.first_app = self.apps.launch(self._first_app)
        self.second_app = self.apps.launch(self._second_app)
        self.third_app = self.apps.launch(self._third_app)

    def test_cards_view(self):

        # switch to top level frame before dispatching the event
        self.marionette.switch_to_frame()

        card_view_element = self.marionette.find_element(*self._cards_view_locator)
        self.assertFalse(card_view_element.is_displayed(),
            "Card view not expected to be visible")

        self._hold_home_button()
        self.wait_for_element_displayed(*self._cards_view_locator)

        self.assertTrue(card_view_element.is_displayed(),
            "Card view expected to be visible")

        first_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._first_app.lower())
        self.assertFalse(first_app_card.is_displayed(), "First opened app should not be visible in cards view")

        second_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._second_app.lower())
        self.assertTrue(second_app_card.is_displayed())

        third_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._third_app.lower())
        self.assertTrue(third_app_card.is_displayed())

        self._touch_home_button()
        self.wait_for_element_not_displayed(*self._cards_view_locator)

        self.assertFalse(card_view_element.is_displayed(),
            "Card view not expected to be visible")

    def test_that_app_can_be_launched_from_cards_view(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/98

        # go to the home screen
        self.marionette.switch_to_frame()
        self._touch_home_button()

        time.sleep(2) # wait for the animation to finish
        self.assertFalse(self.first_app.frame.is_displayed())
        self.assertFalse(self.second_app.frame.is_displayed())
        self.assertFalse(self.third_app.frame.is_displayed())

        # pull up the cards view
        self._hold_home_button()
        self.wait_for_element_displayed(*self._cards_view_locator)

        self.assertFalse(self.first_app.frame.is_displayed())
        self.assertFalse(self.second_app.frame.is_displayed())
        self.assertFalse(self.third_app.frame.is_displayed())


        # launch the app from the cards view
        second_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._second_app.lower())
        self.assertTrue(second_app_card.is_displayed())
        self.marionette.tap(second_app_card)

        self.wait_for_element_not_displayed(*self._cards_view_locator)

        self.assertTrue(self.second_app.frame.is_displayed(),
            "Clock frame was expected to be displayed but was not")

        # check the app order in the cards view
        self._hold_home_button()
        self.wait_for_element_displayed(*self._cards_view_locator)

        first_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._first_app.lower())
        self.assertFalse(first_app_card.is_displayed(), "First opened app should not be visible in cards view")

        second_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._second_app.lower())
        self.assertTrue(second_app_card.is_displayed())

        third_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._third_app.lower())
        self.assertTrue(third_app_card.is_displayed())

    def test_kill_app_from_cards_view(self):
        # go to the home screen
        self.marionette.switch_to_frame()
        self._touch_home_button()

        # pull up the cards view
        self._hold_home_button()
        self.wait_for_element_displayed(*self._cards_view_locator)

        # Find the close icon for the current app
        close_first_app_button = self.marionette.find_element(self._close_button_locator[0], self._close_button_locator[1] %self._third_app.lower())
        self.marionette.tap(close_first_app_button)

        self.marionette.switch_to_frame()

        # pull up the cards view again
        self._hold_home_button()
        self.wait_for_element_displayed(*self._cards_view_locator)

        # If we successfully killed the app, we should no longer find the app
        # card inside cards view.
        self.assertRaises(NoSuchElementException, self.marionette.find_element,
                self._app_card_locator[0], self._app_card_locator[1] %self._third_app.lower())

        # Check if the remaining 2 apps are visible in the cards view
        first_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._first_app.lower())
        self.assertTrue(first_app_card.is_displayed(), "First opened app should not be visible in cards view")

        second_app_card = self.marionette.find_element(self._app_card_locator[0], self._app_card_locator[1] %self._second_app.lower())
        self.assertTrue(second_app_card.is_displayed())

    def _hold_home_button(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")

    def _touch_home_button(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
