# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from gaiatest import GaiaTestCase
import json
import os


class TestPopulateData(GaiaTestCase):

    def add_contacts(self):
        print 'adding contacts'

        for x in range(0, 1000):
            if not x % 100:
                print '\tcontact %d - %d' % (x, x + 99)
            contact = {'name': 'testcontact_%d' % x,
                       'tel': {'type': 'Mobile', 'value': '1-555-522-%d' % x}}

            self.data_layer.insert_contact(contact)

    def push_resource(self, filename, count=1, destination=''):
        local = self.resource(filename)
        remote = '/'.join(['sdcard', destination, local.rpartition(os.path.sep)[-1]])
        self.device.manager.mkDirs(remote)
        self.device.manager.pushFile(local, remote)

        for x in range(0, count):
            if not x % 100:
                print '\tfile %d - %d' % (x, min(x + 99, count))
            remote_copy = '%s_%d%s' % (remote[:remote.find('.')],
                                      x,
                                      remote[remote.find('.'):])
            self.device.manager._checkCmd(['shell',
                                           'dd',
                                           'if=%s' % remote,
                                           'of=%s' % remote_copy])

        self.device.manager.removeFile(remote)

    def add_music(self):
        print 'adding music'
        self.push_resource('MUS_0001.mp3', count=50)

    def add_photos(self):
        print 'adding photos'
        self.push_resource('IMG_fx.jpg', count=70, destination='DCIM/100MZLLA')

    def test_populate_data(self):
        self.add_contacts()
        self.add_music()
        self.add_photos()
