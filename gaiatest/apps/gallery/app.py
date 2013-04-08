# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class Gallery(Base):

    name = 'Gallery'

    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _empty_gallery_title_locator = ('id', 'overlay-title')
    _empty_gallery_text_locator = ('id', 'overlay-text')
    _progress_bar_locator = ('id', 'progress')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._progress_bar_locator)

    def wait_for_files_to_load(self, files_number):
        self.wait_for_condition(lambda m: m.execute_script('return window.wrappedJSObject.files.length') == files_number)

    @property
    def gallery_items_number(self):
        return len(self.marionette.find_elements(*self._gallery_items_locator))

    def tap_first_gallery_item(self):
        first_gallery_item = self.marionette.find_elements(*self._gallery_items_locator)[0]
        self.marionette.tap(first_gallery_item)
        from gaiatest.apps.gallery.regions.fullscreen_image import FullscreenImage
        return FullscreenImage(self.marionette, self.app)

    @property
    def empty_gallery_title(self):
        return self.marionette.find_element(*self._empty_gallery_title_locator).text

    @property
    def empty_gallery_text(self):
        return self.marionette.find_element(*self._empty_gallery_text_locator).text

    @property
    def are_gallery_items_displayed(self):
        return self.marionette.find_element(*self._gallery_items_locator).is_displayed()
