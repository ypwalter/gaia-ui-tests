# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact


class TestContacts(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')

    _settings_button_locator = ('id', 'settings-button')
    _settings_close_button_locator = ('id', 'settings-close')
    _order_by_last_name_locator = ('css selector', 'p[data-l10n-id="contactsOrderBy"]')
    _order_by_last_name_switch_locator = ('css selector', 'input[name="order.lastname"]')
    _contacts_items_locator = ('css selector', '.contact-item p[data-order]')

    # contacts name list
    _contacts_name_list = [('GG', 'E'), ('AA', 'Z'), ('XX', 'C'), ('CC', 'X'), ('EE', 'G'), ('FF', 'F'), ('HH', 'D'), ('BB', 'Y'), ('YY', 'B'), ('ZZ', 'A'), ('DD', 'H')]

    def setUp(self):
        GaiaTestCase.setUp(self)

        # insert contacts by given names
        for contact_name in self._contacts_name_list:
            contact = MockContact(givenName=contact_name[0], familyName=contact_name[1])
            self.data_layer.insert_contact(contact)
        # prepare the sorted-by-first-name and sorted-by-last-name lists
        self.sorted_contacts_name_by_first = sorted(self._contacts_name_list, key=lambda name: name[0])
        self.sorted_contacts_name_by_last = sorted(self._contacts_name_list, key=lambda name: name[1])

        # launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

    def create_contact_locator(self, contact):
        return ('css selector', '.contact-item p[data-order^=%s]' % contact)

    def test_add_photo_from_gallery_to_contact(self):
        """ Test sorting of contacts

        https://github.com/mozilla/gaia-ui-tests/issues/467

        """

        # Make sure the "order-by-last-name" is off before running test
        self.wait_for_element_displayed(*self._settings_button_locator)
        # navigate to settings page
        contact_settings_button = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(contact_settings_button)
        self.wait_for_element_displayed(*self._order_by_last_name_locator)
        order_by_last_name = self.marionette.find_element(*self._order_by_last_name_locator)
        order_by_last_name_switch = self.marionette.find_element(*self._order_by_last_name_switch_locator)
        if order_by_last_name_switch.is_selected():
            # if "Order by last name" switch is on, turn off it
            self.marionette.tap(order_by_last_name)
        # go to contacts main page from settings page
        settings_close_button = self.marionette.find_element(*self._settings_close_button_locator)
        self.marionette.tap(settings_close_button)

        # sort by first name, compare with sorted-by-first-name list
        self.wait_for_element_displayed(*self._settings_button_locator)
        contact_items = self.marionette.find_elements(*self._contacts_items_locator)
        for idx in range(len(self._contacts_name_list)):
            name_tuple = self.sorted_contacts_name_by_first[idx]
            self.assertEqual(contact_items[idx].text, name_tuple[0] + " " + name_tuple[1], "Should order by first name.")

        # navigate to settings page
        contact_settings_button = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(contact_settings_button)
        # turn on "Order by last name" switch
        self.wait_for_element_displayed(*self._order_by_last_name_locator)
        order_by_last_name = self.marionette.find_element(*self._order_by_last_name_locator)
        self.marionette.tap(order_by_last_name)

        # go to contacts main page from settings page
        self.wait_for_element_displayed(*self._settings_close_button_locator)
        settings_close_button = self.marionette.find_element(*self._settings_close_button_locator)
        self.marionette.tap(settings_close_button)

        # sort by last name, compare with sorted-by-last-name list
        self.wait_for_element_displayed(*self._settings_button_locator)
        contact_items = self.marionette.find_elements(*self._contacts_items_locator)
        for idx in range(len(self._contacts_name_list)):
            name_tuple = self.sorted_contacts_name_by_last[idx]
            self.assertEqual(contact_items[idx].text, name_tuple[0] + " " + name_tuple[1], "Should order by last name.")

        # navigate to settings page
        contact_settings_button = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(contact_settings_button)
        # turn off "Order by last name" switch
        self.wait_for_element_displayed(*self._order_by_last_name_locator)
        order_by_last_name = self.marionette.find_element(*self._order_by_last_name_locator)
        self.marionette.tap(order_by_last_name)
