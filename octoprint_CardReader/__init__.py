# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import evdev

class CardreaderPlugin(	octoprint.plugin.StartupPlugin,
												octoprint.plugin.EventHandlerPlugin):
	##~~ Startup Plugin
	def on_after_startup(self):
		devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
		for device in devices:
			self._logger.info(device.fn + "  " + device.name + " " + device.phys)

	##~~ EventHandler Plugin
	def on_event(self, event, payload):
		if event == "PrintStarted":
			self._printer.pause_print()
			self._logger.info("Print Paused")
			for evdevEvent in evdev.InputDevice('/dev/input/event0').read_loop():
				if evdevEvent.type == evdev.ecodes.EV_KEY:
					#self._logger.info(evdevEvent.code)
					if evdevEvent.code <= 11:
						self._logger.info("Number")
					else:
						self._logger.info(evdevEvent.code)
						if evdevEvent.code == 28 and evdevEvent.value == 0:
							break
			self._printer.resume_print()
			self._logger.info("Print Resumed")
				

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Card Reader"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CardreaderPlugin()

