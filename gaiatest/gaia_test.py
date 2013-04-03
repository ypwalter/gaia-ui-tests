# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import base64
import json
import os
import sys
import time
import traceback

from marionette import MarionetteTestCase
from marionette import Marionette
from marionette import MarionetteTouchMixin
from marionette.errors import NoSuchElementException
from marionette.errors import ElementNotVisibleException
from marionette.errors import TimeoutException
from marionette.marionette import Actions
import mozdevice


class LockScreen(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_lock_screen.js"))
        self.marionette.import_script(js)

    @property
    def is_locked(self):
        self.marionette.switch_to_frame()
        return self.marionette.execute_script('window.wrappedJSObject.LockScreen.locked')

    def lock(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script('GaiaLockScreen.lock()')
        assert result, 'Unable to lock screen'

    def unlock(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script('GaiaLockScreen.unlock()')
        assert result, 'Unable to unlock screen'


class GaiaApp(object):

    def __init__(self, origin=None, name=None, frame=None, src=None):
        self.frame = frame
        self.frame_id = frame
        self.src = src
        self.name = name
        self.origin = origin

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class GaiaApps(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)

    def get_permission(self, app_name, permission_name):
        return self.marionette.execute_async_script("return GaiaApps.getPermission('%s', '%s')" % (app_name, permission_name))

    def set_permission(self, app_name, permission_name, value):
        return self.marionette.execute_async_script("return GaiaApps.setPermission('%s', '%s', '%s')" %
                                                    (app_name, permission_name, value))

    def launch(self, name, switch_to_frame=True, url=None):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("GaiaApps.launchWithName('%s')" % name)
        assert result, "Failed to launch app with name '%s'" % name
        app = GaiaApp(frame=result.get('frame'),
                      src=result.get('src'),
                      name=result.get('name'),
                      origin=result.get('origin'))
        if app.frame_id is None:
            raise Exception("App failed to launch; there is no app frame")
        if switch_to_frame:
            self.switch_to_frame(app.frame_id, url)
        return app

    def uninstall(self, name):
        self.marionette.switch_to_frame()
        self.marionette.execute_async_script("GaiaApps.uninstallWithName('%s')" % name)

    def kill(self, app):
        self.marionette.switch_to_frame()
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)
        result = self.marionette.execute_async_script("GaiaApps.kill('%s');" % app.origin)
        assert result, "Failed to kill app with name '%s'" % app.name

    def kill_all(self):
        self.marionette.switch_to_frame()
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)
        self.marionette.execute_async_script("GaiaApps.killAll()")

    def runningApps(self):
        return self.marionette.execute_script("return GaiaApps.getRunningApps()")

    def switch_to_frame(self, app_frame, url=None, timeout=30):
        self.marionette.switch_to_frame(app_frame)
        start = time.time()
        if not url:
            def check(now):
                return "about:blank" not in now
        else:
            def check(now):
                return url in now
        while (time.time() - start < timeout):
            if check(self.marionette.get_url()):
                return
            time.sleep(2)
        raise TimeoutException('Could not switch to app frame %s in time' % app_frame)


class GaiaData(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_data_layer.js"))
        self.marionette.import_script(js)
        self.marionette.set_search_timeout(10000)

    def set_time(self, date_number):
        self.marionette.set_context(self.marionette.CONTEXT_CHROME)
        self.marionette.execute_script("window.navigator.mozTime.set(%s);" % date_number)
        self.marionette.set_context(self.marionette.CONTEXT_CONTENT)

    @property
    def all_contacts(self):
        self.marionette.switch_to_frame()
        return self.marionette.execute_async_script('return GaiaDataLayer.getAllContacts();', special_powers=True)

    def insert_contact(self, contact):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script('return GaiaDataLayer.insertContact(%s);' % json.dumps(contact), special_powers=True)
        assert result, 'Unable to insert contact %s' % contact

    def remove_all_contacts(self, default_script_timeout):
        self.marionette.switch_to_frame()
        self.marionette.set_script_timeout(max(default_script_timeout, 1000 * len(self.all_contacts)))
        result = self.marionette.execute_async_script('return GaiaDataLayer.removeAllContacts();', special_powers=True)
        assert result, 'Unable to remove all contacts'
        self.marionette.set_script_timeout(default_script_timeout)

    def get_setting(self, name):
        return self.marionette.execute_async_script('return GaiaDataLayer.getSetting("%s")' % name, special_powers=True)

    @property
    def all_settings(self):
        return self.get_setting('*')

    def set_setting(self, name, value):
        import json
        value = json.dumps(value)
        result = self.marionette.execute_async_script('return GaiaDataLayer.setSetting("%s", %s)' % (name, value), special_powers=True)
        assert result, "Unable to change setting with name '%s' to '%s'" % (name, value)

    def set_volume(self, value):
        self.set_setting('audio.volume.master', value)

    def enable_cell_data(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("return GaiaDataLayer.enableCellData()", special_powers=True)
        assert result, 'Unable to enable cell data'

    def disable_cell_data(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("return GaiaDataLayer.disableCellData()", special_powers=True)
        assert result, 'Unable to disable cell data'

    @property
    def is_cell_data_connected(self):
        return self.marionette.execute_script("return GaiaDataLayer.isCellDataConnected()")

    def enable_cell_roaming(self):
        self.set_setting('ril.data.roaming_enabled', True)

    def disable_cell_roaming(self):
        self.set_setting('ril.data.roaming_enabled', False)

    def enable_wifi(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("return GaiaDataLayer.enableWiFi()", special_powers=True)
        assert result, 'Unable to enable WiFi'

    def disable_wifi(self):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("return GaiaDataLayer.disableWiFi()", special_powers=True)
        assert result, 'Unable to disable WiFi'

    def connect_to_wifi(self, network):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script("return GaiaDataLayer.connectToWiFi(%s)" % json.dumps(network))
        assert result, 'Unable to connect to WiFi network'

    def forget_all_networks(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_async_script('return GaiaDataLayer.forgetAllNetworks()')

    def is_wifi_connected(self, network):
        self.marionette.switch_to_frame()
        return self.marionette.execute_script("return GaiaDataLayer.isWiFiConnected(%s)" % json.dumps(network))

    @property
    def known_networks(self):
        return self.marionette.execute_async_script('return GaiaDataLayer.getKnownNetworks()')

    @property
    def active_telephony_state(self):
        # Returns the state of only the currently active call or None if no active call
        return self.marionette.execute_script("return GaiaDataLayer.getMozTelephonyState()")

    @property
    def is_antenna_available(self):
        return self.marionette.execute_script('return window.navigator.mozFMRadio.antennaAvailable')

    @property
    def is_fm_radio_enabled(self):
        return self.marionette.execute_script('return window.navigator.mozFMRadio.enabled')

    @property
    def fm_radio_frequency(self):
        return self.marionette.execute_script('return window.navigator.mozFMRadio.frequency')

    @property
    def media_files(self):
        return self.marionette.execute_async_script('return GaiaDataLayer.getAllMediaFiles();')

    def delete_all_sms(self):
        self.marionette.switch_to_frame()
        return self.marionette.execute_async_script("return GaiaDataLayer.deleteAllSms();", special_powers=True)

    def delete_all_alarms(self):
        self.marionette.execute_script('GaiaDataLayer.deleteAllAlarms();')

    def kill_active_call(self):
        self.marionette.execute_script("var telephony = window.navigator.mozTelephony; " +
                                       "if(telephony.active) telephony.active.hangUp();")


class GaiaDevice(object):

    def __init__(self, marionette):
        self.marionette = marionette

    @property
    def manager(self):
        if hasattr(self, '_manager') and self._manager:
            return self._manager

        if not self.is_android_build:
            raise Exception('Device manager is only available for devices.')

        dm_type = os.environ.get('DM_TRANS', 'adb')
        if dm_type == 'adb':
            self._manager = mozdevice.DeviceManagerADB()
        elif dm_type == 'sut':
            host = os.environ.get('TEST_DEVICE')
            if not host:
                raise Exception('Must specify host with SUT!')
            self._manager = mozdevice.DeviceManagerSUT(host=host)
        else:
            raise Exception('Unknown device manager type: %s' % dm_type)
        return self._manager

    @property
    def is_android_build(self):
        return 'Android' in self.marionette.session_capabilities['platform']

    @property
    def has_mobile_connection(self):
        return self.marionette.execute_script('return window.navigator.mozMobileConnection !== undefined')

    def push_file(self, source, count=1, destination='', progress=None):
        if not destination.count('.') > 0:
            destination = '/'.join([destination, source.rpartition(os.path.sep)[-1]])
        self.manager.mkDirs(destination)
        self.manager.pushFile(source, destination)

        if count > 1:
            for i in range(1, count + 1):
                remote_copy = '_%s.'.join(iter(destination.split('.'))) % i
                self.manager._checkCmd(['shell', 'dd', 'if=%s' % destination, 'of=%s' % remote_copy])
                if progress:
                    progress.update(i)

            self.manager.removeFile(destination)

    def restart_b2g(self):
        self.stop_b2g()
        time.sleep(2)
        self.start_b2g()

    def start_b2g(self):
        self.manager.shellCheckOutput(['start', 'b2g'])
        self.marionette.wait_for_port()
        self.marionette.start_session()
        self.marionette.execute_async_script("""
window.addEventListener('mozbrowserloadend', function mozbrowserloadend(aEvent) {
  window.removeEventListener('mozbrowserloadend', mozbrowserloadend);
  marionetteScriptFinished();
});""")

    def stop_b2g(self):
        self.manager.shellCheckOutput(['stop', 'b2g'])
        self.marionette.client.close()
        self.marionette.session = None
        self.marionette.window = None


class GaiaTestCase(MarionetteTestCase):

    _script_timeout = 60000
    _search_timeout = 10000

    # deafult timeout in seconds for the wait_for methods
    _default_timeout = 30

    def setUp(self):
        MarionetteTestCase.setUp(self)
        self.marionette.__class__ = type('Marionette', (Marionette, MarionetteTouchMixin), {})

        self.device = GaiaDevice(self.marionette)
        if self.device.is_android_build:
            self.device.restart_b2g()

        self.marionette.setup_touch()

        # the emulator can be really slow!
        self.marionette.set_script_timeout(self._script_timeout)
        self.marionette.set_search_timeout(self._search_timeout)
        self.lockscreen = LockScreen(self.marionette)
        self.apps = GaiaApps(self.marionette)
        self.data_layer = GaiaData(self.marionette)
        self.keyboard = Keyboard(self.marionette)

        # wifi is true if testvars includes wifi details and wifi manager is defined
        self.wifi = self.testvars and \
            'wifi' in self.testvars and \
            self.marionette.execute_script('return window.navigator.mozWifiManager !== undefined')

        self.cleanUp()

    def cleanUp(self):
        # remove media
        if self.device.is_android_build and self.data_layer.media_files:
            for filename in self.data_layer.media_files:
                self.device.manager.removeFile('/'.join(['sdcard', filename]))

        # disable passcode before restore settings from testvars
        self.data_layer.set_setting('lockscreen.passcode-lock.code', '1111')
        self.data_layer.set_setting('lockscreen.passcode-lock.enabled', False)

        # Change language back to English
        self.data_layer.set_setting("language.current", "en-US")

        # restore settings from testvars
        [self.data_layer.set_setting(name, value) for name, value in self.testvars.get('settings', {}).items()]

        # unlock
        self.lockscreen.unlock()

        # kill any open apps
        self.apps.kill_all()

        # disable sound completely
        self.data_layer.set_volume(0)

        # enable the device radio, disable Airplane mode
        self.data_layer.set_setting('ril.radio.disabled', False)

        # disable carrier data connection
        if self.device.has_mobile_connection:
            self.data_layer.disable_cell_data()

        if self.wifi:
            # forget any known networks
            self.data_layer.enable_wifi()
            self.data_layer.forget_all_networks()
            self.data_layer.disable_wifi()

        # remove data
        self.data_layer.remove_all_contacts(self._script_timeout)

        # reset to home screen
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def push_resource(self, filename, count=1, destination=''):
        self.device.push_file(self.resource(filename), count, '/'.join(['sdcard', destination]))

    def resource(self, filename):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', filename))

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

    def wait_for_element_not_present(self, by, locator, timeout=_default_timeout):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                self.marionette.find_element(by, locator)
            except NoSuchElementException:
                break
        else:
            raise TimeoutException(
                'Element %s still present after timeout' % locator)

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

    def wait_for_condition(self, method, timeout=_default_timeout,
                           message="Condition timed out"):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
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

    def is_element_present(self, by, locator):
        try:
            self.marionette.find_element(by, locator)
            return True
        except:
            return False

    def is_element_displayed(self, by, locator):
        try:
            return self.marionette.find_element(by, locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def tearDown(self):
        if any(sys.exc_info()):
            # test has failed, gather debug
            test_class, test_name = self.marionette.test_name.split()[-1].split('.')
            xml_output = self.testvars.get('xml_output', None)
            debug_path = os.path.join(xml_output and os.path.dirname(xml_output) or 'debug', test_class)
            if not os.path.exists(debug_path):
                os.makedirs(debug_path)

            # screenshot
            try:
                with open(os.path.join(debug_path, '%s_screenshot.png' % test_name), 'w') as f:
                    # TODO: Bug 818287 - Screenshots include data URL prefix
                    screenshot = self.marionette.screenshot()[22:]
                    f.write(base64.decodestring(screenshot))
            except:
                traceback.print_exc()

            # page source
            try:
                with open(os.path.join(debug_path, '%s_source.txt' % test_name), 'w') as f:
                    f.write(self.marionette.page_source.encode('utf-8'))
            except:
                traceback.print_exc()

            # settings
            # Switch to top frame in case we are in a 3rd party app
            # There is no more debug gathering is not specific to the app
            self.marionette.switch_to_frame()

            try:
                with open(os.path.join(debug_path, '%s_settings.json' % test_name), 'w') as f:
                    f.write(json.dumps(self.data_layer.all_settings))
            except:
                traceback.print_exc()

        self.lockscreen = None
        self.apps = None
        self.data_layer = None
        MarionetteTestCase.tearDown(self)


class Keyboard(object):
    _language_key = '-3'
    _numeric_sign_key = '-2'
    _alpha_key = '-1'
    _backspace_key = '8'
    _enter_key = '13'
    _alt_key = '18'
    _upper_case_key = '20'
    _space_key = '32'

    # Keyboard app
    _keyboard_frame_locator = ('css selector', '#keyboard-frame iframe')
    _keyboard_locator = ('css selector', '#keyboard')

    _button_locator = ('css selector', 'button.keyboard-key[data-keycode="%s"]')

    def __init__(self, marionette):
        self.marionette = marionette

    def _switch_to_keyboard(self):
        self.marionette.switch_to_frame()
        keybframe = self.marionette.find_element(*self._keyboard_frame_locator)
        self.marionette.switch_to_frame(keybframe, focus=False)

    def _key_locator(self, val):
        if len(val) == 1:
            val = ord(val)
        return (self._button_locator[0], self._button_locator[1] % val)

    def _tap(self, val):
        key = self.marionette.find_element(*self._key_locator(val))
        self.marionette.tap(key)

    def is_element_present(self, by, locator):
        try:
            self.marionette.set_search_timeout(500)
            self.marionette.find_element(by, locator)
            return True
        except:
            return False
        finally:
            # set the search timeout to the default value
            self.marionette.set_search_timeout(10000)

    def send(self, string):
        self._switch_to_keyboard()

        for val in string:
            # alpha is in on keyboard
            if val.isalpha():
                if self.is_element_present(*self._key_locator(self._alpha_key)):
                    self._tap(self._alpha_key)
                if not self.is_element_present(*self._key_locator(val)):
                    self._tap(self._upper_case_key)
            # numbers and symbols are in another keyboard
            else:
                if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
                    self._tap(self._numeric_sign_key)
                if not self.is_element_present(*self._key_locator(val)):
                    self._tap(self._alt_key)

            # after switching to correct keyboard, tap/click if the key is there
            if self.is_element_present(*self._key_locator(val)):
                self._tap(val)
            else:
                assert False, 'Key %s not found on the keyboard' % val

            # after tap/click space key, it might get screwed up due to timing issue. adding 0.7sec for it.
            if ord(val) == int(self._space_key):
                time.sleep(0.7)

        self.marionette.switch_to_frame()

    def switch_to_number_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._numeric_sign_key)
        self.marionette.switch_to_frame()

    def switch_to_alpha_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._alpha_key)
        self.marionette.switch_to_frame()

    def tap_shift(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._alpha_key)):
            self._tap(self._alpha_key)
        self._tap(self._upper_case_key)
        self.marionette.switch_to_frame()

    def tap_backspace(self):
        self._switch_to_keyboard()
        bs = self.marionette.find_element(self._button_locator[0], self._button_locator[1] % self._backspace_key)
        self.marionette.tap(bs)
        self.marionette.switch_to_frame()

    def tap_space(self):
        self._switch_to_keyboard()
        self._tap(self._space_key)
        self.marionette.switch_to_frame()

    def tap_enter(self):
        self._switch_to_keyboard()
        self._tap(self._enter_key)
        self.marionette.switch_to_frame()

    def tap_alt(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
            self._tap(self._numeric_sign_key)
        self._tap(self._alt_key)
        self.marionette.switch_to_frame()

    def enable_caps_lock(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._alpha_key)):
            self._tap(self._alpha_key)
        key_obj = self.marionette.find_element(*self._key_locator(self._upper_case_key))
        self.marionette.double_tap(key_obj)
        self.marionette.switch_to_frame()

    def long_press(self, key, timeout=2000):
        if len(key) == 1:
            self._switch_to_keyboard()
            key_obj = self.marionette.find_element(*self._key_locator(key))
            self.marionette.long_press(key_obj, timeout)
            time.sleep(timeout / 1000 + 1)
            self.marionette.switch_to_frame()

    # This is for selecting special characters after long pressing
    # "selection" is the nth special element you want to select
    # "movement" is when you don't like it to move toward list or when there is no list
    def choose_extended_character(self, long_press_key, selection, movement=True):
        self._switch_to_keyboard()

        action = Actions(self.marionette)
        key = self._key_locator(long_press_key)
        # alpha is in on keyboard
        if long_press_key.isalpha():
            if self.is_element_present(*self._key_locator(self._alpha_key)):
                self._tap(self._alpha_key)
            if not self.is_element_present(*key):
                self._tap(self._upper_case_key)
        # numbers and symbols are in another keyboard
        else:
            if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
                self._tap(self._numeric_sign_key)
            if not self.is_element_present(*key):
                self._tap(self._alt_key)

        # after switching to correct keyboard, set long press if the key is there
        if self.is_element_present(*key):
            keyobj = self.marionette.find_element(*key)
            action.press(keyobj).perform()
            time.sleep(1)
        else:
            assert False, 'Key %s not found on the keyboard' % val

        # find the extended key and perform the action chain
        extend_keys = self.marionette.find_elements('css selector', 'div.highlighted button')
        action.move(extend_keys[selection - 1]).release().perform()
        self.marionette.switch_to_frame()
