# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact

from marionette.errors import NoSuchElementException


class TestContacts(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')
    _contacts_frame_locator = ('css selector', "iframe[src='app://communications.gaiamobile.org/contacts/index.html']")

    # Header buttons
    _done_button_locator = ('id', 'save-button')
    _edit_contact_button_locator = ('id', 'edit-contact-button')
    _details_back_button_locator = ('id', 'details-back')

    # Contact details panel
    _contact_name_title = ('id', 'contact-name-title')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    # New/Edit contact fields
    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _phone_field_locator = ('id', "number_0")
    _add_picture_link_locator = ('id', 'thumbnail-photo')

    # Select from: dialog
    _gallery_button_locator = ('css selector', "a[data-value='0']")

    # Gallery
    _gallery_frame_locator = ('css selector', "iframe[src='app://gallery.gaiamobile.org/index.html#pick']")
    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _gallery_crop_done_button_locator = ('id', 'crop-done-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.contact = MockContact()
        self.data_layer.insert_contact(self.contact)

        # launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

    def create_contact_locator(self, contact):
        return ('css selector', '.contact-item p[data-search^=%s]' % contact)

    def test_edit_contact(self):
        # https://moztrap.mozilla.org/manage/case/1310/
        # First insert a new contact to edit

        contact_locator = self.create_contact_locator(self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        contact_listing = self.marionette.find_element(*contact_locator)
        self.marionette.tap(contact_listing)

        self.wait_for_element_displayed(*self._edit_contact_button_locator)
        edit_contact = self.marionette.find_element(*self._edit_contact_button_locator)
        self.marionette.tap(edit_contact)

        # Now we'll update the mock contact and then insert the new values into the UI
        self.contact['givenName'] = 'gaia%s' % repr(time.time()).replace('.', '')[10:]
        self.contact['familyName'] = "testedit"
        self.contact['tel']['value'] = "02011111111"

        self.wait_for_element_displayed(*self._given_name_field_locator)
        given_name_field = self.marionette.find_element(*self._given_name_field_locator)
        given_name_field.clear()
        given_name_field.send_keys(self.contact['givenName'])

        family_name_field = self.marionette.find_element(*self._family_name_field_locator)
        family_name_field.clear()
        family_name_field.send_keys(self.contact['familyName'])

        tel_field = self.marionette.find_element(*self._phone_field_locator)
        tel_field.clear()
        tel_field.send_keys(self.contact['tel']['value'])

        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)

        # Construct a new locator using the edited givenName
        edited_contact_locator = self.create_contact_locator(self.contact['givenName'])

        details_back_button = self.marionette.find_element(*self._details_back_button_locator)
        self.marionette.tap(details_back_button)

        # click back into the contact
        self.wait_for_element_displayed(*edited_contact_locator)

        edited_contact = self.marionette.find_element(*edited_contact_locator)

        # Due to a previous issue this will check that the original contact is no longer present
        self.assertRaises(NoSuchElementException,
                          self.marionette.find_element, contact_locator[0], contact_locator[1])

        self.assertTrue(edited_contact.is_displayed(),
                        "Expected the edited contact to be present")

        self.marionette.tap(edited_contact)

        # Now assert that the values have updated
        full_name = self.contact['givenName'] + " " + self.contact['familyName']

        self.assertEqual(self.marionette.find_element(*self._contact_name_title).text,
                         full_name)
        self.assertEqual(self.marionette.find_element(*self._call_phone_number_button_locator).text,
                         self.contact['tel']['value'])

    def test_add_photo_from_gallery_to_contact(self):
        # https://moztrap.mozilla.org/manage/case/5551/

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        contact_locator = self.create_contact_locator(self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        contact_listing = self.marionette.find_element(*contact_locator)
        self.marionette.tap(contact_listing)

        self.wait_for_element_displayed(*self._edit_contact_button_locator)
        edit_contact = self.marionette.find_element(*self._edit_contact_button_locator)
        self.marionette.tap(edit_contact)

        self.wait_for_element_displayed(*self._add_picture_link_locator)
        picture_link = self.marionette.find_element(*self._add_picture_link_locator)
        saved_picture_style = picture_link.get_attribute('style')
        self.marionette.tap(picture_link)

        # switch to the system app
        self.marionette.switch_to_frame()

        # choose the source as gallery app
        self.wait_for_element_displayed(*self._gallery_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._gallery_button_locator))

        # switch to the gallery app
        self.wait_for_element_displayed(*self._gallery_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._gallery_frame_locator))

        self.wait_for_element_displayed(*self._gallery_items_locator)
        gallery_items = self.marionette.find_elements(*self._gallery_items_locator)
        self.assertGreater(len(gallery_items), 0, 'No photos were found in the gallery.')
        self.marionette.tap(gallery_items[0])

        self.wait_for_element_displayed(*self._gallery_crop_done_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._gallery_crop_done_button_locator))

        # switch back to the contacts app
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._contacts_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._contacts_frame_locator))
        self.wait_for_element_displayed(*self._add_picture_link_locator)

        new_picture_style = self.marionette.find_element(*self._add_picture_link_locator).get_attribute('style')
        self.assertNotEqual(new_picture_style, saved_picture_style,
                            'The picture associated with the contact was not changed.')
