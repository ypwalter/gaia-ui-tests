# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class SearchResults(Base):

    _search_results_area_locator = ('id', 'search-results')
    _search_result_locator = ('css selector', '#search-results li.item')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._search_results_area_locator)

    @property
    def search_results(self):
        return [self.Result(marionette=self.marionette, element=result)
                for result in self.marionette.find_elements(*self._search_result_locator)]

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
