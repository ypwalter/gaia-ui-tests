# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest.apps.base import Base


class Gallery(Base):

    name = "Gallery"

    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_image_locator = ('css selector', '#frames > div.frame[style ~= "translateX(0px);"] > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')
    _empty_gallery_title_locator = ('id', 'overlay-title')
    _empty_gallery_text_locator = ('id', 'overlay-text')
    _progress_bar_locator = ('id', 'progress')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._progress_bar_locator)

    @property
    def gallery_items(self):
        return self.marionette.find_elements(*self._gallery_items_locator)

    @property
    def first_gallery_item(self):
        return self.marionette.find_elements(*self._gallery_items_locator)[0]

    def tap_first_gallery_item(self):
        self.marionette.tap(self.first_gallery_item)
        self.wait_for_element_displayed(*self._current_image_locator)

    @property
    def current_image(self):
        return self.marionette.find_element(*self._current_image_locator)

    @property
    def current_image_source(self):
        return self.marionette.find_element(*self._current_image_locator).get_attribute('src')

    @property
    def is_photo_toolbar_visible(self):
        return self.marionette.find_element(*self._photos_toolbar_locator).is_displayed()

    @property
    def empty_gallery_title(self):
        return self.marionette.find_element(*self._empty_gallery_title_locator).text

    @property
    def empty_gallery_text(self):
        return self.marionette.find_element(*self._empty_gallery_text_locator).text

    def flick_to_image(self, direction):
        self.marionette.flick(self.current_image,  # target element
                              '50%', '50%',  # start from middle of the target element
                              '%s50%%' % (direction == 'previous' and '+' or direction == 'next' and '-'), 0,  # move 50% of width to the left/right
                              800)  # gesture duration
        self.wait_for_element_displayed(*self._current_image_locator)
        # TODO
        # remove sleep after Bug 843202 - Flicking through images in gallery crashes the app is fixed
        time.sleep(1)
