# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestYouTube(GaiaTestCase):

    video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_play_youtube_video(self):
        """ Confirm YouTube video playback

        https://moztrap.mozilla.org/manage/case/6073/

        """
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url(self.video_URL)
        browser.switch_to_content()

        # Tap the video
        fullscreen_video = browser.tap_video()

        # Switch to video player
        fullscreen_video.switch_to_video_frame()

        # Check for playback
        self.assertTrue(fullscreen_video.is_video_playing)
