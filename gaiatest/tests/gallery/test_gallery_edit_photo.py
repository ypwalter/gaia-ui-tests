# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import time

from gaiatest import GaiaTestCase


class TestGalleryEditPhoto(GaiaTestCase):

    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_image_locator = ('css selector', '#frame2 > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')

    _edit_photo_locator = ('id', 'fullscreen-edit-button')
    _edit_effect_button_locator = ('id', 'edit-effect-button')
    _effect_options_locator = ('css selector', '#edit-effect-options a')
    _edit_save_locator = ('id', 'edit-save-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_edit_photo(self):

        self.wait_for_element_displayed(*self._gallery_items_locator)

        gallery_items = self.marionette.find_elements(*self._gallery_items_locator)
        old_count = len(gallery_items)
        self.assertTrue(old_count > 0)

        self.marionette.tap(gallery_items[0])
        self.wait_for_element_displayed(*self._current_image_locator)

        current_image = self.marionette.find_element(*self._current_image_locator)
        photos_toolbar = self.marionette.find_element(*self._photos_toolbar_locator)

        self.assertIsNotNone(current_image.get_attribute('src'))
        self.assertTrue(photos_toolbar.is_displayed())

        # Tap on Edit button
        self.wait_for_element_displayed(*self._edit_photo_locator)
        edit_photo_button = self.marionette.find_element(*self._edit_photo_locator)
        self.marionette.tap(edit_photo_button)

        # Tap on Effects button
        self.wait_for_element_displayed(*self._edit_effect_button_locator)
        edit_effect_button = self.marionette.find_element(*self._edit_effect_button_locator)
        self.marionette.tap(edit_effect_button)

        # Change effects
        self.wait_for_element_displayed(*self._effect_options_locator)
        effects = self.marionette.find_elements(*self._effect_options_locator)

        previous_image_source = None
        for e in effects:
            self.marionette.tap(e)
            # Wait until the current effect is selected.
            self.wait_for_condition(lambda m: 'selected' in e.get_attribute('class'))

            # TBD. Verify the photo is changed.

        edit_save_button = self.marionette.find_element(*self._edit_save_locator)
        self.marionette.tap(edit_save_button)

        # Verify new Photo is created
        self.wait_for_element_displayed(*self._gallery_items_locator)
        self.wait_for_condition(lambda m: len(self.marionette.find_elements(*self._gallery_items_locator)) == 2)
