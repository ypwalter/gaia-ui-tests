# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from marionette import MarionetteTestOptions
from marionette import MarionetteTestRunner
from marionette.runtests import cli


class GaiaTestOptions(MarionetteTestOptions):

    def __init__(self, **kwargs):
        MarionetteTestOptions.__init__(self, **kwargs)
        group = self.add_option_group('gaiatest')
        group.add_option('--restart',
                         action='store_true',
                         dest='restart',
                         default=False,
                         help='restart target instance between tests')


class GaiaTestRunner(MarionetteTestRunner):

    def register_handlers(self):
        self.test_handlers.extend([GaiaTestCase])


def main():
    cli(runner_class=GaiaTestRunner, parser_class=GaiaTestOptions)


if __name__ == "__main__":
    main()
