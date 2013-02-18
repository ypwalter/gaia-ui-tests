# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base


class Phone(Base):

    name = "Phone"

    @property
    def dialer(self):
        from gaiatest.apps.phone.regions.dialer import Dialer
        return Dialer(self.marionette)

    def call_screen(self, dialing_app):
        from gaiatest.apps.phone.regions.call_screen import CallScreen
        return CallScreen(self.marionette, dialing_app)
