# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from gaiatest.apps.gallery.app import Gallery


class TestGallery(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_view(self):
        # https://moztrap.mozilla.org/manage/case/1326/

        gallery = Gallery(self.marionette)
        gallery.launch()

        gallery.tap_first_gallery_item()

        self.assertIsNotNone(gallery.current_image_source)
        self.assertTrue(gallery.is_photo_toolbar_visible)

        # TODO
        # Add steps to view picture full screen
        # TODO
        # Repeat test with landscape orientation
