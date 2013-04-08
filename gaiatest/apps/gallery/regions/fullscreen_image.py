# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest.apps.base import Base


class FullscreenImage(Base):

    _current_image_locator = ('css selector', '#frames > div.frame[style ~= "translateX(0px);"] > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')
    _delete_image_locator = ('id', 'fullscreen-delete-button')
    _confirm_delete_locator = ('id', 'modal-dialog-confirm-ok')
    _edit_photo_locator = ('id', 'fullscreen-edit-button')
    _tile_view_locator = ('id', 'fullscreen-back-button')

    def __init__(self, marionette, app):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._current_image_locator)
        self.app = app

    @property
    def is_photo_toolbar_displayed(self):
        return self.marionette.find_element(*self._photos_toolbar_locator).is_displayed()

    @property
    def current_image_source(self):
        return self.marionette.find_element(*self._current_image_locator).get_attribute('src')

    def flick_to_next_image(self):
        self._flick_to_image('next')

    def flick_to_previous_image(self):
        self._flick_to_image('previous')

    def _flick_to_image(self, direction):
        current_image = self.marionette.find_element(*self._current_image_locator)
        self.marionette.flick(current_image,  # target element
                              '50%', '50%',  # start from middle of the target element
                              '%s50%%' % (direction == 'previous' and '+' or direction == 'next' and '-'), 0,  # move 50% of width to the left/right
                              800)  # gesture duration
        self.wait_for_element_displayed(*self._current_image_locator)
        # TODO
        # remove sleep after Bug 843202 - Flicking through images in gallery crashes the app is fixed
        time.sleep(1)

    def tap_delete_button(self):
        self.marionette.tap(self.marionette.find_element(*self._delete_image_locator))
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._confirm_delete_locator)

    def tap_confirm_deletion_button(self):
        self.marionette.tap(self.marionette.find_element(*self._confirm_delete_locator))
        self.wait_for_element_not_displayed(*self._confirm_delete_locator)
        self.marionette.switch_to_frame(self.app.frame)

    def tap_edit_button(self):
        self.marionette.tap(self.marionette.find_element(*self._edit_photo_locator))
        from gaiatest.apps.gallery.regions.edit_photo import EditPhoto
        return EditPhoto(self.marionette)

    def tap_tile_view_button(self):
        self.marionette.tap(self.marionette.find_element(*self._tile_view_locator))
        from gaiatest.apps.gallery.app import Gallery
        return Gallery(self.marionette)
