# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class FmRadio(Base):
    name = 'FM Radio'

    _power_button_locator = ('id', 'power-switch')
    _favorite_list_locator = ('css selector', 'div.fav-list-item')
    _frequency_display_locator = ('id', 'frequency')
    _frequency_dialer_locator = ('id', 'frequency-dialer')
    _favorite_button_locator = ('id', 'bookmark-button')
    _next_button_locator = ('id', 'frequency-op-seekup')
    _prev_button_locator = ('id', 'frequency-op-seekdown')

    def flick_frequency_dialer_up(self):
        dialer = self.marionette.find_element(*self._frequency_dialer_locator)

        dialer_x_center = int(dialer.size['width'] / 2)
        dialer_y_center = int(dialer.size['height'] / 2)
        self.marionette.flick(dialer, dialer_x_center, dialer_y_center, 0, 300, 800)

    def tap_next(self):
        current_frequency = self.frequency
        self.marionette.tap(self.marionette.find_element(*self._next_button_locator))
        self.wait_for_condition(lambda m: self.frequency != current_frequency)

    def tap_previous(self):
        current_frequency = self.frequency
        self.marionette.tap(self.marionette.find_element(*self._prev_button_locator))
        self.wait_for_condition(lambda m: self.frequency != current_frequency)

    def tap_power_button(self):
        self.marionette.tap(self.marionette.find_element(*self._power_button_locator))

    def wait_for_radio_off(self):
        self.wait_for_condition(lambda m:self.is_power_button_on is False )

    def tap_add_favorite(self):
        current_favorite_channel_count = len(self.favorite_channels)
        self.marionette.tap(self.marionette.find_element(*self._favorite_button_locator))
        self.wait_for_condition(lambda m: current_favorite_channel_count + 1 == len(self.favorite_channels))

    def wait_for_favorite_list_not_displayed(self):
        self.wait_for_element_not_displayed(*self._favorite_list_locator)

    @property
    def is_power_button_on(self):
        return self.marionette.find_element(*self._power_button_locator).get_attribute('data-enabled') == 'true'

    @property
    def frequency(self):
        return float(self.marionette.find_element(*self._frequency_display_locator).text)

    @property
    def favorite_channels(self):
        return [self.FavoriteChannel(self.marionette, channel) for channel in self.marionette.find_elements(*self._favorite_list_locator)]

    class FavoriteChannel(PageRegion):
        _remove_locator = ('css selector', 'div.fav-list-remove-button')
        _frequency_locator = ('css selector', 'div.fav-list-frequency')

        @property
        def text(self):
            return float(self.root_element.find_element(*self._frequency_locator).text)

        def remove(self):
            self.marionette.tap(self.root_element.find_element(*self._remove_locator))
