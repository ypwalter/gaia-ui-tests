# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.mocks.mock_contact_given_name import MockContactGivenName


class TestContacts(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')
    _contacts_frame_locator = ('css selector', "iframe[src='app://communications.gaiamobile.org/contacts/index.html']")

    _settings_button_locator = ("id", "settings-button")
    _settings_close_button_locator = ("id", "settings-close")
    _order_by_last_name_locator = ('css selector', 'p[data-l10n-id="contactsOrderBy"]')
    _contacts_items_locator = ('css selector', '.contact-item p[data-order]')

    _contacts_name_list = [("AA", "Z"), ("BB", "Y"), ("CC", "X"), ("DD", "H"), ("EE", "G"), ("FF", "F"), ("GG", "E"), ("HH", "D"), ("XX", "C"), ("YY", "B"), ("ZZ", "A")]


    def setUp(self):
        GaiaTestCase.setUp(self)

        for contact_name in self._contacts_name_list:
            contact = MockContactGivenName(*contact_name)
            self.data_layer.insert_contact(contact)
        
        self.sorted_contacts_name_by_given = sorted(self._contacts_name_list, key=lambda name: name[0])
        self.sorted_contacts_name_by_family = sorted(self._contacts_name_list, key=lambda name: name[1])
        
        # launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

    def create_contact_locator(self, contact):
        return ('css selector', '.contact-item p[data-order^=%s]' % contact)

    def test_add_photo_from_gallery_to_contact(self):
        """ Test sorting of contacts
        
        https://github.com/mozilla/gaia-ui-tests/issues/467
        
        """
        
        # TODO check the value of "Order by last name" switch, then compare with order-by-first-name or order-by-last-name
        
        # sort by first name
        self.wait_for_element_displayed(*self._settings_button_locator)
        contact_items = self.marionette.find_elements(*self._contacts_items_locator)
        for idx in range(len(self._contacts_name_list)):
            name_tuple = self.sorted_contacts_name_by_given[idx]
            self.assertEqual(contact_items[idx].text, name_tuple[0] + " " + name_tuple[1], "Should order by first name.") 

        # navigate to settings page
        contact_settings_button = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(contact_settings_button)
        # turn on "Order by last name" switch
        self.wait_for_element_displayed(*self._order_by_last_name_locator)
        _order_by_last_name_button = self.marionette.find_element(*self._order_by_last_name_locator)
        self.marionette.tap(_order_by_last_name_button)

        # go to contacts main page from settings page
        self.wait_for_element_displayed(*self._settings_close_button_locator)
        settings_close_button = self.marionette.find_element(*self._settings_close_button_locator)
        self.marionette.tap(settings_close_button)
        
        # sort by last name 
        self.wait_for_element_displayed(*self._settings_button_locator)
        contact_items = self.marionette.find_elements(*self._contacts_items_locator)
        for idx in range(len(self._contacts_name_list)):
            name_tuple = self.sorted_contacts_name_by_family[idx]
            self.assertEqual(contact_items[idx].text, name_tuple[0] + " " + name_tuple[1], "Should order by last name.")
        
        # navigate to settings page
        contact_settings_button = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(contact_settings_button)
        # turn off "Order by last name" switch
        self.wait_for_element_displayed(*self._order_by_last_name_locator)
        _order_by_last_name_button = self.marionette.find_element(*self._order_by_last_name_locator)
        self.marionette.tap(_order_by_last_name_button)
