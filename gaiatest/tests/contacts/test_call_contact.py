# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact

from gaiatest.apps.contacts.app import Contacts


class TestContacts(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Seed the contact with the remote phone number so we don't call random people
        self.contact = MockContact(tel={
            'type': 'Mobile',
            'value': "%s" % self.testvars['remote_phone_number']})
        self.data_layer.insert_contact(self.contact)

    def test_call_contact(self):
        # NB This is not a listed smoke test
        # Call phone from a contact
        # https://moztrap.mozilla.org/manage/case/5679/

        contacts = Contacts(self.marionette)
        contacts.launch()

        # tap on the created contact
        contact_details = contacts.contact(self.contact['givenName']).tap()

        # tap the phone number and switch to call screen frame
        call_screen = contact_details.tap_phone_number()

        call_screen.wait_for_outgoing_call()

        # Check the number displayed is the one we dialed
        self.assertIn(self.contact['tel']['value'],
                      call_screen.outgoing_calling_contact)

        # TODO: This is no longer appearing on the call screen. Xfailing due to bug #869060
        self.assertIn(self.contact['givenName'],
                      call_screen.calling_contact_information)

        call_screen.hang_up()
        # Switch back to main frame before Marionette loses track bug #840931
        self.marionette.switch_to_frame()

    def tearDown(self):

        # In case the assertion fails this will still kill the call
        # An open call creates problems for future tests
        self.data_layer.kill_active_call()

        GaiaTestCase.tearDown(self)
