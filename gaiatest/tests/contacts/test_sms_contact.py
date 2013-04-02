# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact

from gaiatest.apps.contacts.app import Contacts


class TestContacts(GaiaTestCase):

    _sms_app_iframe_locator = ('css selector', 'iframe[src^="app://sms"][src$="index.html"]')

    #SMS app locators
    _sms_app_header_locator = ('id', 'header-text')
    _contact_carrier_locator = ('id', 'contact-carrier')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.contact = MockContact()
        self.data_layer.insert_contact(self.contact)

    def test_sms_contact(self):
        # https://moztrap.mozilla.org/manage/case/1314/
        # Setup a text message from a contact

        contacts = Contacts(self.marionette)
        contacts.launch()

        # tap on the created contact
        contact_details = contacts.contact(self.contact['givenName']).tap()

        contact_details.tap_send_sms()

        self.marionette.switch_to_frame()

        sms_iframe = self.marionette.find_element(*self._sms_app_iframe_locator)
        self.marionette.switch_to_frame(sms_iframe)

        self.wait_for_condition(
            lambda m: m.find_element(*self._contact_carrier_locator).text != "Carrier unknown")

        header_element = self.marionette.find_element(*self._sms_app_header_locator)
        expected_name = self.contact['givenName'] + " " + self.contact['familyName']
        expected_tel = self.contact['tel']['value']

        self.assertEqual(header_element.text, expected_name)
        self.assertEqual(header_element.get_attribute('data-phone-number'),
                         expected_tel)
