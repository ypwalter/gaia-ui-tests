# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import time


class TestFtu(GaiaTestCase):

    _next_button_locator = ('id', 'forward')

    _section_languages_locator = ('id', 'languages')
    _section_cell_data_locator = ('id', 'data_3g')
    _section_wifi_locator = ('id', 'wifi')
    _section_date_time_locator = ('id', 'date_and_time')
    _section_import_contacts_locator = ('id', 'import_contacts')
    _section_ayr_locator = ('id', 'about-your-rights')
    _section_welcome_browser_locator = ('id', 'welcome_browser')
    _section_browser_privacy_locator = ('id', 'browser_privacy')
    _section_finish_locator = ('id', 'finish-screen')

    _take_tour_button_locator = ('id', 'lets-go-button')

    # Section Tour
    _step1_header_locator = ('id', 'step1Header')
    _step2_header_locator = ('id', 'step2Header')
    _step3_header_locator = ('id', 'step3Header')
    _step4_header_locator = ('id', 'step4Header')
    _step5_header_locator = ('id', 'step5Header')
    _tour_next_button_locator = ('id', 'forwardTutorial')
    _tour_back_button_locator = ('id', 'backTutorial')

    # Section Tutorial Finish
    _section_tutorial_finish_locator = ('id', 'tutorialFinish')
    _lets_go_button_locator = ('id', 'tutorialFinished')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the First Time User app
        self.app = self.apps.launch('FTU')

    def test_ftu_with_tour(self):

        self.wait_for_element_displayed(*self._section_languages_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_cell_data_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_wifi_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_date_time_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_import_contacts_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_welcome_browser_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_browser_privacy_locator)
        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_finish_locator)

        # Take the tour
        self.marionette.find_element(*self._take_tour_button_locator).click()

        # Walk through the tour
        self.wait_for_element_displayed(*self._step1_header_locator)
        self.assertEqual(self.marionette.find_element(*self._step1_header_locator).text,
                         "Swipe from right to left to browse your apps.")
        self.marionette.find_element(*self._tour_next_button_locator).click()
        self.wait_for_element_displayed(*self._step2_header_locator)
        self.assertEqual(self.marionette.find_element(*self._step2_header_locator).text,
                         "Swipe from left to right to discover new apps.")
        self.marionette.find_element(*self._tour_next_button_locator).click()
        self.wait_for_element_displayed(*self._step3_header_locator)
        self.assertEqual(self.marionette.find_element(*self._step3_header_locator).text,
                         "Tap and hold on an icon to delete or move it.")
        self.marionette.find_element(*self._tour_next_button_locator).click()
        self.wait_for_element_displayed(*self._step4_header_locator)
        self.assertEqual(self.marionette.find_element(*self._step4_header_locator).text,
                         "Swipe down to access recent notifications, credit information and settings.")
        self.marionette.find_element(*self._tour_next_button_locator).click()
        self.wait_for_element_displayed(*self._step5_header_locator)
        self.assertEqual(self.marionette.find_element(*self._step5_header_locator).text,
                         "Tap and hold the home button to browse and close recent apps.")
        # Try going back a step
        self.marionette.find_element(*self._tour_back_button_locator).click()
        self.wait_for_element_displayed(*self._step4_header_locator)
        self.marionette.find_element(*self._tour_next_button_locator).click()
        self.wait_for_element_displayed(*self._step5_header_locator)
        self.marionette.find_element(*self._tour_next_button_locator).click()

        self.wait_for_element_displayed(*self._section_tutorial_finish_locator)
        self.marionette.find_element(*self._lets_go_button_locator).click()

        # Switch back to top level now that FTU app is gone
        self.marionette.switch_to_frame()

    def tearDown(self):

        # TODO flush any settings set by the FTU app
        self.data_layer.disable_cell_data()

        self.data_layer.disable_wifi()

        GaiaTestCase.tearDown(self)
