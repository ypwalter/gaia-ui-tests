# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class SettingsForm(Base):

    _settings_close_button_locator = ('id', 'settings-close')
    _order_by_last_name_locator = ('css selector', 'p[data-l10n-id="contactsOrderBy"]')
    _order_by_last_name_switch_locator = ('css selector', 'input[name="order.lastname"]')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_settings_close_button_to_load()

    def wait_for_settings_close_button_to_load(self):
        self.wait_for_element_displayed(*self._settings_close_button_locator)

    def tap_order_by_last_name(self):
        self.marionette.tap(self.marionette.find_element(*self._order_by_last_name_locator))

    @property
    def order_by_last_name(self):
        return self.marionette.find_element(*self._order_by_last_name_switch_locator).is_selected()

    def tap_done(self):
        self.marionette.tap(self.marionette.find_element(*self._settings_close_button_locator))
        from gaiatest.apps.contacts.app import Contacts
        return Contacts(self.marionette)
