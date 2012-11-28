Contribution is more than welcome!

This suite of tests is currently focused upon replicating manual tests listed
in [MozTrap](https://moztrap.mozilla.org/).

First timers
============
You will need either an emulator or device (phone) with a Marionette-enabled
build installed on it. This is a difficult step but you can find help on [MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Building_and_installing_Firefox_OS)

A good place to get started is to run the tests. This will give you experience
in the relationship between the tests and the device or emulator.
Refer to the README.md in this repository and the [MDN Marionette resource](https://developer.mozilla.org/en-US/docs/Marionette/Marionette_Python_Tests).

Experienced Testers
===================
If you already know what you're doing then your first port of call is the Git
issues to find an issue to work on. Please mark it or comment in it to let us
know you're working on it.

Resources
=========
The Marionette MDN resource contains up to date information on running
tests and all of the commands available:
https://developer.mozilla.org/en-US/docs/Marionette

Style Guide
===========
At the moment we don't have a specific style guide. Please follow the
prevailing style of the existing tests. Use them as a template for writing
your tests.

Device or Emulator?
===================
We welcome tests that run on both emulator and physical devices.
Some tests can only be run on the emulator and vice versa, often depending
upon hardware requirements.
An example of this is setting the charged state of the battery - on the
emulator the battery level can be set and tested against in Firefox OS.

We use a manifest file to filter tests based upon the hardware requirements
(for example WiFi, SIM card, etc). The manifest file is set with the marks
we need. Please set your test in the manifest file so that we know to run it
on the appropriate device.

Pull Requests
=============
Submit your pull request to us via GitHub, marking it with a reference to the
Git issue or MozTrap test case to give us context to the code.

Contacting us
=============
You can find us and other Mozillians that can help out in #appsqa on the
irc.mozilla.org network. We work primarily across EU and PST timezones.

Feel free to contact us with any queries you may have. We're here to help with
problems of any nature.
