# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class RemoveConfirm(Base):

    _form_locator = ('id', 'confirmation-message')
    _cancel_locator = ('xpath', '//form[@id="confirmation-message"]//menu//button[text()="Cancel"]')
    _remove_locator = ('xpath', '//form[@id="confirmation-message"]//menu//button[text()="Remove"]')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._form_locator)

    def tap_cancel(self):
        self.marionette.tap(self.marionette.find_element(*self._cancel_locator))
        from gaiatest.apps.contacts.regions.contact_form import EditContact
        return EditContact(self.marionette)

    def tap_remove(self):
        self.marionette.tap(self.marionette.find_element(*self._remove_locator))
        from gaiatest.apps.contacts.app import Contacts
        return Contacts(self.marionette)
