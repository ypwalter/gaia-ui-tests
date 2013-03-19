# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.phone.app import Phone

class TestDialerAddContact(GaiaTestCase):

    # Dialer app
    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _add_new_contact_button_locator = ('id', 'keypad-callbar-add-contact')
    _contacts_view_locator = ('id','option-contacts')

    # Header buttons
    _done_button_locator = ('id', 'save-button')
    _loading_overlay = ('id', 'loading-overlay')
    _details_back_button_locator = ('id', 'details-back')
    _edit_contact_button_locator = ('id', 'edit-contact-button')

    # New/Edit contact fields
    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _phone_field_locator = ('id', 'number_0')

    # Contact details panel
    _contact_name_title = ('id', 'contact-name-title')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    # frames
    _new_contact_frame_locator=('css selector',"iframe[src='app://communications.gaiamobile.org/contacts/index.html?new']")
    _contact_frame_locator=('css selector','#iframe-contacts')
    _keyboard_frame_locator=('css selector',"iframe[src='app://communications.gaiamobile.org/dialer/index.html#keyboard-view']")

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.contact = MockContact()

        # launch the Phone app
        self.phone = Phone(self.marionette)
        self.phone.launch()

    def test_dialer_add_contact(self):

        self.wait_for_element_displayed(*self._keyboard_container_locator)

        # Dial number
        test_phone_number = '+86123456789'
        self.phone.keypad.phone_number = test_phone_number

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(*self._phone_number_view_locator)
        self.assertEqual(phone_view.get_attribute('value'), test_phone_number)

        # Click Add contact button
        self.wait_for_element_displayed(*self._add_new_contact_button_locator)
        add_new_contact = self.marionette.find_element(*self._add_new_contact_button_locator)
        self.marionette.tap(add_new_contact)

        # Add new contact page is open
        self.wait_for_element_not_displayed(*self._loading_overlay)

        time.sleep(5)

        # Switch to add contacts frame
        self.marionette.switch_to_frame()
        new_contact_frame=self.marionette.find_element(*self._new_contact_frame_locator)
        self.marionette.switch_to_frame(new_contact_frame)

        # Enter data into fields
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])

        # Click Done button
        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)

        # Switch back to keyboard-view
        self.marionette.switch_to_frame()
        keyboard_frame=self.marionette.find_element(*self._keyboard_frame_locator)
        self.marionette.switch_to_frame(keyboard_frame)

        #Go to Contact list and Verify result
        contact_view=self.marionette.find_element(*self._contacts_view_locator)
        self.marionette.tap(contact_view)

        time.sleep(2)

        # switch to contact frame
        contact_frame=self.marionette.find_element(*self._contact_frame_locator)
        self.marionette.switch_to_frame(contact_frame)

        # Check only on econtact is created
        contact_list = self.marionette.find_elements('css selector','#contacts-list-G li')
        self.assertEqual(1,len(contact_list))

        #  Tap on the new contact
        contact = contact_list[0]
        self.marionette.tap(contact)

        time.sleep(2)

        # Now assert that the values have updated
        full_name = self.contact['givenName'] + " " + self.contact['familyName']

        # Need an extra wait as this is failing intermittently
        self.wait_for_condition(lambda m: m.find_element(*self._contact_name_title).text == full_name)

        self.assertEqual(self.marionette.find_element(*self._contact_name_title).text,
                         full_name)

        # Verify Phone number
        self.assertEqual(self.marionette.find_element(*self._call_phone_number_button_locator).text,
                         test_phone_number)

        # click back into the contact
        details_back_button = self.marionette.find_element(*self._details_back_button_locator)
        self.marionette.tap(details_back_button)

    def tearDown(self):
        GaiaTestCase.tearDown(self)
