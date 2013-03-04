# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts


class TestContacts(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.contact = MockContact()

    def test_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/
        #click Create new contact

        # launch the Contacts app
        contacts_app = Contacts(self.marionette)
        contacts_app.launch()

        new_contact_form = contacts_app.tap_new_contact()

        # Enter data into fields
        new_contact_form.given_name = self.contact['givenName']
        new_contact_form.family_name = self.contact['familyName']

        new_contact_form.phone_field = self.contact['tel']['value']
        new_contact_form.email_field = self.contact['email']
        new_contact_form.street_field = self.contact['street']
        new_contact_form.zip_code_field = self.contact['zip']
        new_contact_form.city_field = self.contact['city']
        new_contact_form.country_field = self.contact['country']
        new_contact_form.comment_field = self.contact['comment']

        contacts_app = new_contact_form.tap_done()
        self.wait_for_condition(lambda m: len(contacts_app.contacts) == 1)

        self.assertEqual(contacts_app.contacts[0].name, self.contact['givenName'])
