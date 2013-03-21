# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.gallery.app import Gallery


class TestGallery(GaiaTestCase):

    images = 'IMG_0001.jpg'
    image_count = 4
    image1 = 'IMG_0001.jpg'
    image2 = 'IMG_0002.jpg'
    image3 = 'IMG_0003.jpg'
    image4 = 'IMG_0004.jpeg'
    _current_image_locator = ('css selector', '#frame2 > img')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photos to storage
        #self.push_resource(self.images, self.image_count, 'DCIM/100MZLLA')
        self.push_resource(self.image1, destination = 'DCIM/100MZLLA')
        self.push_resource(self.image2, destination = 'DCIM/100MZLLA')
        self.push_resource(self.image3, destination = 'DCIM/100MZLLA')
        self.push_resource(self.image4, destination = 'DCIM/100MZLLA')

    def test_gallery_full_screen_image_flicks(self):
        # https://moztrap.mozilla.org/manage/case/1326/

        gallery = Gallery(self.marionette)
        gallery.launch()

        self.assertEqual(len(gallery.gallery_items), self.image_count)

        # tap first image to open full screen view
        gallery.tap_first_gallery_item()

        previous_image_source = None

        # Check the next flicks
        #for item in gallery.gallery_items:
        for i in range(len(gallery.gallery_items)):
            self.assertIsNotNone(gallery.current_image_source)
            #self.assertNotEqual(gallery.current_image_source, previous_image_source)
            self.assertTrue(gallery.is_photo_toolbar_visible)
            print i
            print previous_image_source
            print gallery.current_image_source
            previous_image_source = gallery.current_image_source
            gallery.flick_to_image('next')

        self.assertIsNotNone(gallery.current_image_source)
        self.assertEqual(gallery.current_image_source, previous_image_source)
        self.assertTrue(gallery.is_photo_toolbar_visible)

        previous_image_source = gallery.current_image_source

        # check the prev flick
        for image in gallery.gallery_items:

            gallery.flick_to_image('previous')
            self.assertIsNotNone(gallery.current_image_source)
            self.assertNotEqual(gallery.current_image_source, previous_image_source)
            self.assertTrue(gallery.is_photo_toolbar_visible)

            previous_image_source = gallery.current_image_source

        # try to flick prev image (No image should be available)
        self.assertIsNotNone(gallery.current_image_source)
        self.assertNotEqual(gallery.current_image_source, previous_image_source)
        self.assertTrue(gallery.is_photo_toolbar_visible)

    # def flick_to_image(self, direction):
        # self.assertTrue(direction in ['previous', 'next'])
        # current_image = self.marionette.find_element(*self._current_image_locator)
        # self.marionette.flick(current_image,  # target element
        #                       '50%', '50%',  # start from middle of the target element
        #                       '%s50%%' % (direction == 'previous' and '+' or direction == 'next' and '-'), 0,  # move 50% of width to the left/right
        #                       800)  # gesture duration
        # self.wait_for_element_not_displayed(*self._current_image_locator)
        # # TODO
        # # remove sleep after Bug 843202 - Flicking through images in gallery crashes the app is fixed
        # time.sleep(1)