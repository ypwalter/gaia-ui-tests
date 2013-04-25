# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestSettingsDoNotTrack(GaiaTestCase):

    # donottrack Settings locators
    _donottrack_menu_item_locator = ('id', "menuItem-doNotTrack")
    _donottrack_label_locator = ('css selector', "#doNotTrack label")
    _donottrack_checkbox_locator = ('css selector', "#doNotTrack input")

    def setUp(self):

        GaiaTestCase.setUp(self)

        # make sure donottrack is off for the beginning of the test
        self.data_layer.set_setting('privacy.donottrackheader.enabled', False)

        # launch the Settings app
        self.app = self.apps.launch('Settings')

    def test_enable_do_not_track_via_settings_app(self):
        """ Enable do not track via the Settings app"""

        # navigate to donodonottrack_checkbox_locatorttrack settings
        self.wait_for_element_present(*self._donottrack_menu_item_locator)
        donottrack_menu_item = self.marionette.find_element(*self._donottrack_menu_item_locator)

        # scroll to the menu item
        self.marionette.execute_script("arguments[0].scrollIntoView(false);",
                                       [donottrack_menu_item])
        self.marionette.tap(donottrack_menu_item)

        # locate the do-not-track label and checkbox
        self.wait_for_element_displayed(*self._donottrack_label_locator)
        donottrack_label = self.marionette.find_element(*self._donottrack_label_locator)
        donottrack_checkbox = self.marionette.find_element(*self._donottrack_checkbox_locator)

        # turned off by default
        self.wait_for_condition(lambda m: donottrack_checkbox.get_attribute('checked') is None)

        # turn on - tap on the label
        self.marionette.tap(donottrack_label)
        self.wait_for_condition(lambda m: donottrack_checkbox.get_attribute('checked'))

        # should be on
        self.assertTrue(self.data_layer.get_setting('privacy.donottrackheader.enabled'),
                        "Do Not Track was not enabled via Settings app")

        # turn back off
        self.marionette.tap(donottrack_label)
        self.wait_for_condition(lambda m: donottrack_checkbox.get_attribute('checked') is None)

        # should be on
        self.assertFalse(self.data_layer.get_setting('privacy.donottrackheader.enabled'),
                         "Do Not Track was not disabled via Settings app")
