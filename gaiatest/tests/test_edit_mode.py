# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from marionette.errors import NoSuchElementException


class TestEditMode(GaiaTestCase):

    _delete_app_locator = ('css selector', 'li.icon > span.options')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.homescreen = self.apps.launch('Homescreen')

    def test_access_and_leave_edit_mode(self):

        self._go_to_next_page()

        # go to edit mode.
        # TODO: activate edit mode using HOME button https://bugzilla.mozilla.org/show_bug.cgi?id=814425
        self._activate_edit_mode()

        #verify that the delete app icons appear
        delete_app_icon = self.marionette.find_element(*self._delete_app_locator)
        self.assertTrue(delete_app_icon.is_displayed())

        #tap home button and verify that delete app icons are no longer visible
        self._touch_home_button()
        self.assertEqual(len(self.marionette.find_elements(*self._delete_app_locator)), 0)

    def _touch_home_button(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def _activate_edit_mode(self):
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")
