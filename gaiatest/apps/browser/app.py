# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import time

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Browser(Base):

    name = "Browser"

    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    # Awesome bar/url bar
    _awesome_bar_locator = ('id', 'url-input')
    _url_button_locator = ('id', 'url-button')
    _throbber_locator = ('id', 'throbber')

    # Tab list area
    _tab_badge_locator = ('id', 'tabs-badge')
    _tabs_number_locator = ('css selector', '#toolbar-start > span')
    _new_tab_button_locator = ('id', 'new-tab-button')
    _tabs_list_locator = ('css selector', '#tabs-list > ul li a')

    # Browser footer
    _back_button_locator = ('id', 'back-button')
    _forward_button_locator = ('id', 'forward-button')
    _bookmark_button_locator = ('id', 'bookmark-button')

    # Bookmark menu
    _bookmark_menu_locator = ('id', 'bookmark-menu')
    _add_bookmark_to_home_screen_choice_locator = ('id', 'bookmark-menu-add-home')

    # System app - add bookmark to homescreen dialog
    _add_bookmark_to_home_screen_frame_locator = ('css selector', 'iframe[src^="app://homescreen"][src$="save-bookmark.html"]')
    _add_bookmark_to_home_screen_dialog_button_locator = ('id', 'button-bookmark-add')
    _bookmark_title_input_locator = ('id', 'bookmark-title')

    def launch(self):
        Base.launch(self)
        self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))

    def go_to_url(self, url):
        self.wait_for_element_displayed(*self._awesome_bar_locator)
        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.clear()
        awesome_bar.send_keys(url)

        self.tap_go_button()

    @property
    def url(self):
        return self.marionette.execute_script("return window.wrappedJSObject.Browser.currentTab.url;")

    def switch_to_content(self):
        web_frames = self.marionette.find_elements(*self._browser_frame_locator)
        for web_frame in web_frames:
            if web_frame.is_displayed():
                self.marionette.switch_to_frame(web_frame)
                break

    def switch_to_chrome(self):
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

    def tap_go_button(self):
        self.marionette.tap(self.marionette.find_element(*self._url_button_locator))
        self.wait_for_throbber_not_visible()
        self.wait_for_element_displayed(*self._bookmark_button_locator)

    def tap_back_button(self):
        current_url = self.url
        self.marionette.tap(self.marionette.find_element(*self._back_button_locator))
        self.wait_for_condition(lambda m: self.url != current_url)

    def tap_forward_button(self):
        current_url = self.url
        self.marionette.tap(self.marionette.find_element(*self._forward_button_locator))
        self.wait_for_condition(lambda m: self.url != current_url)

    def tap_bookmark_button(self):
        self.marionette.tap(self.marionette.find_element(*self._bookmark_button_locator))
        self.wait_for_element_displayed(*self._bookmark_menu_locator)

    def tap_add_bookmark_to_home_screen_choice_button(self):
        self.wait_for_element_displayed(*self._add_bookmark_to_home_screen_choice_locator)
        self.marionette.tap(self.marionette.find_element(*self._add_bookmark_to_home_screen_choice_locator))
        # Switch to System app where the add bookmark dialog resides
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._add_bookmark_to_home_screen_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._add_bookmark_to_home_screen_frame_locator))
        self.wait_for_element_displayed(*self._bookmark_title_input_locator)

    def tap_add_bookmark_to_home_screen_dialog_button(self):
        self.wait_for_element_displayed(*self._add_bookmark_to_home_screen_dialog_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._add_bookmark_to_home_screen_dialog_button_locator))
        self.switch_to_chrome()

    def type_bookmark_title(self, value):
        element = self.marionette.find_element(*self._bookmark_title_input_locator)
        element.clear()
        element.send_keys(value)

    def wait_for_throbber_not_visible(self):
        # TODO see if we can reduce this timeout in the future. >10 seconds is poor UX
        self.wait_for_condition(lambda m: not self.is_throbber_visible, timeout=20)

    @property
    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).get_attribute('class') == 'loading'

    @property
    def is_awesome_bar_visible(self):
        return self.marionette.find_element(*self._awesome_bar_locator).is_displayed()

    def tap_tab_badge_button(self):
        self.marionette.tap(self.marionette.find_element(*self._tab_badge_locator))

        # TODO Wait for visibility when Marionette can detect the state of the tab list correctly
        self.wait_for_condition(lambda m: self._current_screen == 'tabs-screen')

    def tap_add_new_tab_button(self):
        self.marionette.tap(self.marionette.find_element(*self._new_tab_button_locator))

        # TODO Wait for visibility when Marionette can detect the state of the tab list correctly
        self.wait_for_condition(lambda m: self._current_screen == 'awesome-screen')

    @property
    def displayed_tabs_number(self):
        displayed_number = self.marionette.find_element(*self._tabs_number_locator).text
        return int(re.match(r'\d+', displayed_number).group())

    @property
    def tabs_count(self):
        return len(self.marionette.find_elements(*self._tabs_list_locator))

    @property
    def tabs(self):
        return [self.Tab(marionette=self.marionette, element=tab)
                for tab in self.marionette.find_elements(*self._tabs_list_locator)]

    @property
    def _current_screen(self):
        return self.marionette.execute_script("return window.wrappedJSObject.Browser.currentScreen;")

    class Tab(PageRegion):

        def tap_tab(self):
            # TODO replace with self.marionette.tap(self.root_element)
            self.root_element.click()

            # TODO This wait is a workaround until Marionette can correctly interpret the displayed state
            self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.currentScreen;") == 'page-screen')
