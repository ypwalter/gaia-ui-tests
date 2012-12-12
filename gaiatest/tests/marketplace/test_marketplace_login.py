# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestMarketplaceLogin(GaiaTestCase):

    # Marketplace locators
    _login_button = ('css selector', 'a.button.browserid')
    _logged_in_locator = ('css selector', 'div.account.authenticated')
    _settings_cog_locator = ('css selector', 'a.header-button.settings')
    _settings_form_locator = ('css selector', 'form.form-grid')
    _email_account_field_locator = ('id', 'email')
    _logout_button = ('css selector', 'a.logout')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # launch the app
        self.app = self.apps.launch('Marketplace')

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/

        self.wait_for_element_displayed(*self._login_button)

        self.marionette.find_element(*self._login_button).click()

        self._login_to_persona(self.testvars['marketplace']['username'],
                                self.testvars['marketplace']['password'])

        #Switch back to marketplace and verify that user is logged in
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame_id)

        # If you go to fast here marionette seems to clash with marketplace
        time.sleep(3)
        self.wait_for_element_present(*self._logged_in_locator)

        # click the cog
        self.marionette.find_element(*self._settings_cog_locator).click()

        self.wait_for_element_displayed(*self._settings_form_locator)

        self.assertEqual(self.testvars['marketplace']['username'],
            self.marionette.find_element(*self._email_account_field_locator).get_attribute('value'))

        self.marionette.find_element(*self._logout_button).click()
        self.wait_for_element_not_present(*self._logged_in_locator)


    def _login_to_persona(self, username, password):

        _persona_frame = ('css selector', "iframe[name='__persona_dialog']")

        # Persona dialog
        _waiting_locator = ('css selector', 'body.waiting')
        _email_input_locator = ('id', 'email')
        _password_input_locator = ('id', 'password')
        _next_button_locator = ('css selector', 'button.start')
        _returning_button_locator = ('css selector', 'button.returning')
        _sign_in_button_locator = ('id', 'signInButton')

        # switch to top level frame then Persona frame
        self.marionette.switch_to_frame()
        persona_frame = self.wait_for_element_present(*_persona_frame)
        self.marionette.switch_to_frame(persona_frame)

        # Wait for the loading to complete
        self.wait_for_element_not_present(*_waiting_locator)

        if self.is_element_present(*self._email_account_field_locator):
            # Persona has no memory of your details ie after device flash
            email_field = self.marionette.find_element(*_email_input_locator)
            email_field.send_keys(username)

            self.marionette.find_element(*_next_button_locator).click()

            self.wait_for_element_displayed(*_password_input_locator)
            password_field = self.marionette.find_element(*_password_input_locator)
            password_field.send_keys(password)

            self.wait_for_element_displayed(*_returning_button_locator)
            self.marionette.find_element(*_returning_button_locator).click()

        else:
            # Persona remembers your username and password
            self.marionette.find_element(*_sign_in_button_locator).click()


    def tearDown(self):

        # in the event that the test fails, a 2nd attempt
        # switch to marketplace frame and if we are logged in attempt to log out again
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame_id)

        if self.is_element_present(*self._logged_in_locator):
            # Refresh to get back to the marketplace main page
            self.marionette.refresh()

            # click the cog
            self.marionette.find_element(*self._settings_cog_locator).click()
            self.wait_for_element_displayed(*self._settings_form_locator)
            self.marionette.find_element(*self._logout_button).click()

        # close the app
        if self.app:
            self.apps.kill(self.app)

        if self.wifi:
            self.data_layer.disable_wifi()

        GaiaTestCase.tearDown(self)
