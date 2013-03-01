# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Contacts(Base):

    name = "Contacts"

    _loading_overlay = ('id', 'loading-overlay')

    #  contacts
    _contact_locator = ('css selector', 'li.contact-item')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._loading_overlay)

    @property
    def contact_details(self):
        from gaiatest.apps.contacts.regions.contact_details import ContactDetails
        return ContactDetails(self.marionette)

    def contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact

    @property
    def contacts(self):
        return [self.Contact(marionette=self.marionette, element=contact)
                for contact in self.marionette.find_elements(*self._contact_locator)]

    class Contact(PageRegion):

        _name_locator = ('css selector', 'p > strong')
        _tap_locator = ('css selector', 'p > span.org')

        @property
        def name(self):
            return self.root_element.find_element(*self._name_locator).text

        def tap(self):
            self.marionette.tap(self.root_element)

            from gaiatest.apps.contacts.regions.contact_details import ContactDetails

            contact_details = ContactDetails(self.marionette)
            contact_details.wait_for_contact_details_to_load()
            return contact_details
