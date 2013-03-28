# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.phone.app import Phone


class CallLog(Phone):

    _call_log_locator = ('css selector', "iframe[name='call_screen0']")

    _all_calls_tab_locator = ('id', 'allFilter')
    _all_calls_tab_link_locator = ('css selector', '#allFilter a')
    _all_calls_list_item_locator = ('css selector', 'li.log-item')

    def __init__(self, marionette):
        Phone.__init__(self, marionette)
        self.wait_for_element_displayed(*self._all_calls_tab_locator)

    def tap_all_calls_tab(self):
        self.marionette.tap(self.marionette.find_element(*self._all_calls_tab_link_locator))

    @property
    def is_all_calls_tab_selected(self):
        return self.marionette.find_element(*self._all_calls_tab_locator).get_attribute('class') == 'selected'

    @property
    def all_calls_count(self):
        return len(self._all_calls)

    @property
    def is_first_all_call_displayed(self):
        return self._all_calls[0].is_displayed()

    @property
    def _all_calls(self):
        return self.marionette.find_elements(*self._all_calls_list_item_locator)
