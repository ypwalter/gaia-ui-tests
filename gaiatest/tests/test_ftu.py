# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import time

class TestFtu(GaiaTestCase):

    _activation_section_locator = ('id', 'activation')
    _main_title_locator = ('id', 'main_title')


    _next_button_locator = ('id', 'forward')


    # Step 1 Languages section
    _section_languages_locator = ('id', 'languages')
    _listed_languages_locator = ('css selector', "#languages ul li input[name='language.current']")

    # Step 2 Cell data section
    _section_cell_data_locator = ('id', 'data_3g')
    _enable_data_checkbox_locator = ('id', 'dataSwitch')

    # Step 3 Wifi
    _section_wifi_locator = ('id', 'wifi')
    _found_wifi_networks_locator = ('css selector', 'ul#networks li')

    # Step 4 Date & Time
    _section_date_time_locator = ('id', 'date_and_time')
    _timezone_configuration_locator = ('id', 'timezone-configuration')
    _time_zone_title_locator = ('id', 'time-zone-title')

    # Section 5 Import contacts
    _section_import_contacts_locator = ('id', 'import_contacts')
    _import_from_sim_locator = ('id', 'sim_import')
    _sim_import_feedback_locator = ('id', 'sim_import_feedback')

    # Section 6 About Your rights
    _section_ayr_locator = ('id', 'about-your-rights')

    # Section Welcome Browser
    _section_welcome_browser_locator = ('id', 'welcome_browser')
    _enable_statistic_checkbox_locator = ('css selector', 'input[name="enable_statistic"]')

    # Section Privacy Choices
    _section_browser_privacy_locator = ('id', 'browser_privacy')
    _email_field_locator = ('css selector', 'input[type="email"]')

    # Section Finish
    _section_finish_locator = ('id', 'finish')
    _skip_tour_button_locator = ('id', 'skip')

    # Section Tutorial Finish
    _section_tutorial_finish_locator = ('id', 'tutorialFinish')
    _lets_go_button_locator = ('id', 'tutorialFinished')


    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.lockscreen.unlock()

        #if self.data_layer.is_wifi_connected(self.testvars['wifi']):

        self.data_layer.forget_wifi(self.testvars['wifi'])
        self.data_layer.disable_cell_data()

        time.sleep(30)

        # launch the Calculator app
        self.app = self.apps.launch('FTU')



    def test_ftu(self):
        # https://


        self.wait_for_element_displayed(*self._section_languages_locator)

        listed_languages = self.marionette.find_elements(*self._listed_languages_locator)
        self.assertGreater(len(listed_languages), 0, "No languages listed on screen")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_cell_data_locator)

        # Click enable data
        self.marionette.find_element(*self._enable_data_checkbox_locator).click()

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_wifi_locator)

        # Wait for some networks to be found
        self.wait_for_condition(lambda m: len(m.find_elements(*self._found_wifi_networks_locator)) > 0,
                message="No networks listed on screen")

        wifi_network = self.marionette.find_element('id', self.testvars['wifi']['ssid'])
        wifi_network.click()

        self.wait_for_condition(lambda m: wifi_network.find_element('xpath', 'p[2]').text == "connected")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_date_time_locator)

        # Set timezone
        timezone_select = self.marionette.find_element(*self._timezone_configuration_locator)
        timezone_select.click()

        timezone_option = timezone_select.find_element('css selector', "option[value='-5']")
        self._select(timezone_option)

        self.assertEqual(self.marionette.find_element(*self._time_zone_title_locator).text,
                        "GMT-05:00")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_import_contacts_locator)

        # click import from SIM
        # You can do this as many times as you like without db conflict
        self.marionette.find_element(*self._import_from_sim_locator).click()

        # TODO What if Sim has two contacts?
        self.wait_for_condition(lambda m: m.find_element(*self._sim_import_feedback_locator).text ==
                        "Imported one contact", message="Contact did not import from sim before timeout")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_welcome_browser_locator)

        # Don't think this is functional but we'll click it anyway
        # TODO assert via settings API that this is set
        self.marionette.find_element(*self._enable_statistic_checkbox_locator).click()

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_browser_privacy_locator)

        # TODO assert that this is preserved in the system somewhere by checking pref/etc
        self.marionette.find_element(*self._email_field_locator).send_keys("testuser@mozilla.com")

        # Click next
        self.marionette.find_element(*self._next_button_locator).click()
        self.wait_for_element_displayed(*self._section_finish_locator)

       # The tour appears to be empty so let's skip it
        self.marionette.find_element(*self._skip_tour_button_locator).click()

        self.marionette.switch_to_frame()

        self.assertTrue(self.data_layer.get_setting("ril.data.enabled"), "Cell data was not enabled by FTU app")
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via FTU app")

    def tearDown(self):

        # TODO flush any settings set by the FTU app

        self.data_layer.disable_cell_data()
        #self.data_layer.disable_wifi()

        GaiaTestCase.tearDown(self)

    def _select(self, option_element):
        # Cheeky Select wrapper until Marionette has its own one
        # Due to the way B2G wraps the select box it can only match on text
        match_string = option_element.text

        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        ok_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        for li in options:
            if li.text == match_string:
                li.click()
                break

        ok_button.click()

        # Now back to app
        self.marionette.switch_to_frame(self.app.frame_id)
