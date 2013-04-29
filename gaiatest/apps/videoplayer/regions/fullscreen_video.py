# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class FullscreenVideo(Base):

    _video_controls_locator = ('id', 'videoControls')
    _video_title_locator = ('id', 'video-title')
    _elapsed_text_locator = ('id', 'elapsed-text')
    _video_title_locator = ('id', 'video-title')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._video_controls_locator)

    def tap_control_bar(self):
        self.marionette.tap(self.marionette.find_element(*self._video_controls_locator))
        self.wait_for_element_displayed(*self._elapsed_text_locator)

    @property
    def elapsed_time(self):
        return self.marionette.find_element(*self._elapsed_text_locator).text

    @property
    def name(self):
        return self.marionette.find_element(*self._video_title_locator).text
