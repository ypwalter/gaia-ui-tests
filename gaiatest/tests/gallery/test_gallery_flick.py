# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.gallery.app import Gallery


class TestGallery(GaiaTestCase):

    images = 'IMG_0001.jpg'
    image_count = 4

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photos to storage
        self.push_resource(self.images, self.image_count, 'DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_full_screen_image_flicks(self):
        # https://moztrap.mozilla.org/manage/case/1326/

        gallery = Gallery(self.marionette)
        gallery.launch()

        self.assertEqual(len(gallery.gallery_items), self.image_count)

        # tap first image to open full screen view
        gallery.tap_first_gallery_item()

        previous_image_source = None

        # Check the next flicks
        for image in gallery.gallery_items:
            self.assertIsNotNone(image.current_image_source)
            self.assertNotEqual(image.current_image_source, previous_image_source)
            self.assertTrue(image.is_photo_toolbar_visible)

            previous_image_source = image.current_image_source
            gallery.flick_to_image('next')

        self.assertIsNotNone(gallery.current_image_source)
        self.assertEqual(gallery.current_image_source, previous_image_source)
        self.assertTrue(gallery.is_photo_toolbar_visible)

        previous_image_source = gallery.current_image_source

        # check the prev flick
        for image in gallery.gallery_items:

            self.flick_to_image('previous')
            self.assertIsNotNone(image.current_image_source)
            self.assertNotEqual(image.current_image_source, previous_image_source)
            self.assertTrue(image.is_photo_toolbar_visible)

            previous_image_source = gallery.current_image_source

        # try to flick prev image (No image should be available)
        self.assertIsNotNone(gallery.current_image_source)
        self.assertNotEqual(gallery.current_image_source, previous_image_source)
        self.assertTrue(gallery.is_photo_toolbar_visible)

