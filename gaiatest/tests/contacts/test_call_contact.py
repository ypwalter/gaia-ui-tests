# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact

from gaiatest.apps.contacts.app import Contacts
from gaiatest.apps.phone.regions.call_screen import CallScreen


class TestContacts(GaiaTestCase):

    # Contact details panel
    _contact_name_title = ('id', 'contact-name-title')
    _call_phone_number_button_locator = ('id', 'call-or-pick-0')

    # Call Screen app
    # TODO if this step fails bug 817291 may have been fixed
    # Change this locator for the one commented below
    _calling_number_locator = ('css selector', "div.additionalContactInfo")
    #_calling_number_locator = ('css selector', "div.number")
    _outgoing_call_locator = ('css selector', 'div.direction.outgoing')
    _hangup_bar_locator = ('id', 'callbar-hang-up-action')
    _call_app_locator = ('css selector', "iframe[name='call_screen']")

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
        contacts.contact(self.contact['givenName']).tap()
        contacts.contact_details.wait_for_contact_details_to_load

        # tap the phone number
        contacts.contact_details.tap_phone_number()

        # Switch to call screen frame
        call_screen = CallScreen(self.marionette)

        # Wait for call screen then switch to it
        call_screen.wait_for_outgoing_call()

        # Check the number displayed is the one we dialed
        # TODO if this step fails bug 817291 may have been fixed
        self.assertIn(self.contact['tel']['value'],
                      call_screen.calling_contact_information)

        self.assertIn(self.contact['givenName'],
                      call_screen.outgoing_calling_contact[:-1])
        # hang up before the person answers ;)
        call_screen.hang_up()
        # Switch back to main frame before Marionette loses track bug #840931
        self.marionette.switch_to_frame()

    def tearDown(self):

        # In case the assertion fails this will still kill the call
        # An open call creates problems for future tests
        self.data_layer.kill_active_call()

        GaiaTestCase.tearDown(self)
