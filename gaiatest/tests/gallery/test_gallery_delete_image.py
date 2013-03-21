# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestGalleryDelete(GaiaTestCase):

    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_image_locator = ('css selector', '#frame2 > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')
    _delete_image_locator = ('id', 'fullscreen-delete-button')
    _confirm_delete_locator = ('id', 'modal-dialog-confirm-ok')

    _empty_gallery_title_locator = ('id', 'overlay-title')
    _empty_gallery_text_locator = ('id', 'overlay-text')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_delete_image(self):

        # wait for gallery item to be displayed
        self.wait_for_element_displayed(*self._gallery_items_locator)

        gallery_item = self.marionette.find_element(*self._gallery_items_locator)

        # tap image to open full screen view
        self.marionette.tap(gallery_item)
        self.wait_for_element_displayed(*self._current_image_locator)
        self.wait_for_element_displayed(*self._photos_toolbar_locator)

        # tap the delete button from the fullscreen toolbar
        delete_button = self.marionette.find_element(*self._delete_image_locator)
        self.marionette.tap(delete_button)

        self.marionette.switch_to_frame()

        # wait for delete dialog to appear and tap the confirm delete button
        self.wait_for_element_displayed(*self._confirm_delete_locator)
        confirm_delete_button = self.marionette.find_element(*self._confirm_delete_locator)
        self.marionette.tap(confirm_delete_button)

        self.marionette.switch_to_frame(self.app.frame)

        # Wait for the empty gallery overlay to render
        self.wait_for_element_displayed(*self._empty_gallery_title_locator)
        self.wait_for_element_displayed(*self._empty_gallery_text_locator)

        # Verify empty gallery title
        self.assertEqual(self.marionette.find_element(*self._empty_gallery_title_locator).text,
                         "No photos or videos")

        # Verify empty gallery text
        self.assertEqual(self.marionette.find_element(*self._empty_gallery_text_locator).text,
                         "Use the Camera app to get started.")
