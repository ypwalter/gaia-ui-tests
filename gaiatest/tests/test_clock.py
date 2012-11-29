# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestClock(GaiaTestCase):

    _alarm_create_new_locator = ('id', 'alarm-new')
    _alarm_save_locator = ('id', 'alarm-done')
    _banner_countdown_notification_locator = ('id', 'banner-countdown')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        # launch the Clock app
        self.app = self.apps.launch('Clock')

    def test_create_new_alarm(self):
        # https://moztrap.mozilla.org/manage/case/1772/

        self.wait_for_element_displayed(*self._alarm_create_new_locator)

        # create a new alarm with the default values that are avaliable
        self.marionette.find_element(*self._alarm_create_new_locator).click()
        self.marionette.find_element(*self._alarm_save_locator).click()

        # verify the banner-countdown message appears
        self.wait_for_element_displayed(*self._banner_countdown_notification_locator)
        alarm_msg = self.marionette.find_element(*self._banner_countdown_notification_locator).text
        self.assertTrue('The alarm is set for' in alarm_msg, 'Actual banner message was: "' + alarm_msg + '"')

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
