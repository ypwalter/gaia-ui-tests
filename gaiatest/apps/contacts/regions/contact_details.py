# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.contacts.app import Contacts


class ContactDetails(Contacts):

    _contact_name_title = ('id', 'contact-name-title')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    def __init__(self, marionette):
        Contacts.__init__(self, marionette)
        self.wait_for_contact_details_to_load()

    def wait_for_contact_details_to_load(self):
        self.wait_for_element_displayed(*self._call_phone_number_button_locator)

    def tap_phone_number(self):
        self.marionette.tap(self.marionette.find_element(*self._call_phone_number_button_locator))
        from gaiatest.apps.phone.regions.call_screen import CallScreen
        return CallScreen(self.marionette)
