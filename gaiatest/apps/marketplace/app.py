# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys
from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Marketplace(Base):

    name = 'Marketplace'

    _loading_fragment_locator = ('css selector', 'div.loading-fragment')
    _error_title_locator = ('css selector', '#appError-appframe1 h3[data-l10n-id="error-title"]')
    _error_message_locator = ('css selector', '#appError-appframe1 span[data-l10n-id="error-message"]')

    # Marketplace search on home page
    _search_locator = ('id', 'search-q')

    # Marketplace search results area and a specific result item
    _search_results_area_locator = ('id', 'search-results')
    _search_result_locator = ('css selector', '#search-results li.item')

    # System app confirmation button to confirm installing an app
    _yes_button_locator = ('id', 'app-install-install-button')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._loading_fragment_locator)

    @property
    def error_title_text(self):
        return self.marionette.find_element(*self._error_title_locator).text

    @property
    def error_message_text(self):
        return self.marionette.find_element(*self._error_message_locator).text

    def search(self, term):
        search_box = self.marionette.find_element(*self._search_locator)

        if not search_box.is_displayed():
            # Scroll a little to make the search box appear
            self.marionette.execute_script('window.scrollTo(0, 10)')

        # search for the app
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)
        self.wait_for_element_displayed(*self._search_results_area_locator)

    @property
    def search_results(self):
        return [self.Result(marionette=self.marionette, element=result)
                for result in self.marionette.find_elements(*self._search_result_locator)]

    def confirm_installation(self):
        self.wait_for_element_displayed(*self._yes_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._yes_button_locator))
        self.wait_for_element_not_displayed(*self._yes_button_locator)

    class Result(PageRegion):

        _name_locator = ('css selector', '.info > h3')
        _author_locator = ('css selector', '.info .author')
        _install_button_locator = ('css selector', '.button.product.install')

        @property
        def name(self):
            return self.root_element.find_element(*self._name_locator).text

        @property
        def author(self):
            return self.root_element.find_element(*self._author_locator).text

        @property
        def install_button_text(self):
            return self.root_element.find_element(*self._install_button_locator).text

        def tap_install_button(self):
            self.marionette.tap(self.root_element.find_element(*self._install_button_locator))
            self.marionette.switch_to_frame()
