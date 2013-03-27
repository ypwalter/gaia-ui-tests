# -*- coding: utf-8 -*-
from gaiatest import GaiaTestCase

class TestEverythingMeSearchAccented(GaiaTestCase):

  def setUp(self):
    GaiaTestCase.setUp(self)
    self.apps.set_permission('Homescreen', 'geolocation', 'deny')

    if self.wifi:
        self.data_layer.enable_wifi()
        self.data_layer.connect_to_wifi(self.testvars['wifi'])

    self.lockscreen.unlock()


  def test_launch_everything_me_search_accented(self):
    hs_frame = self.marionette.find_element('css selector', 'div.homescreen > iframe')
    self.marionette.switch_to_frame(hs_frame)
    self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")

    search_txt = self.marionette.find_element('id', 'search-q');
    search_txt.clear() #clean it first
    search_txt.send_keys(u"Özdemir Erdoğan")

    self.keyboard.tap_enter()

    _shortcut_items_locator = ('css selector', '#shortcuts-items li')

    self.wait_for_element_present(*_shortcut_items_locator)

    shortcuts = self.marionette.find_elements(*_shortcut_items_locator)
    self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')



