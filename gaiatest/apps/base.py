# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.errors import NoSuchElementException
from marionette.errors import TimeoutException

from gaiatest import GaiaApps


class Base(object):
    # deafult timeout in seconds for the wait_for methods
    _default_timeout = 30

    def __init__(self, marionette):
        self.marionette = marionette
        self.apps = GaiaApps(self.marionette)

    def launch(self):
        self.app = self.apps.launch(self.name)

    def wait_for_element_present(self, by, locator, timeout=_default_timeout):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                return self.marionette.find_element(by, locator)
            except NoSuchElementException:
                pass
        else:
            raise TimeoutException(
                'Element %s not found before timeout' % locator)

    def wait_for_element_displayed(self, by, locator, timeout=_default_timeout):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                if self.marionette.find_element(by, locator).is_displayed():
                    break
            except NoSuchElementException:
                pass
        else:
            raise TimeoutException(
                'Element %s not visible before timeout' % locator)

    def wait_for_element_not_displayed(self, by, locator, timeout=_default_timeout):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                if not self.marionette.find_element(by, locator).is_displayed():
                    break
            except NoSuchElementException:
                break
        else:
            raise TimeoutException(
                'Element %s still visible after timeout' % locator)

    def wait_for_condition(self, method, timeout=_default_timeout, message="Condition timed out"):
        """Calls the method provided with the driver as an argument until the return value is not False."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                value = method(self.marionette)
                if value:
                    return value
            except NoSuchElementException:
                pass
            time.sleep(0.5)
        else:
            raise TimeoutException(message)


class PageRegion(Base):
    def __init__(self, marionette, element):
        self.root_element = element
        Base.__init__(self, marionette)
