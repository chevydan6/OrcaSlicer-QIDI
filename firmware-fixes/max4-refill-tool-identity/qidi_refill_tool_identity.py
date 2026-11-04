# MAX4 inlet-refill logical-tool preservation.
# Copyright (C) 2026 Dan and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Scoped workaround for the installed QIDI Box v1 refill index mismatch.

Keep the vendor's selection, flush, loading and resume implementation. Intercept
only its erroneous extrude_state write inside AUTO_RELOAD_FUNC. Firmware hashes
are pinned because this deliberately wraps an internal vendor implementation.
"""
import functools
import hashlib
import logging
import os

VERSION = '1'
_FIRMWARE_DIRECTORY = os.path.dirname(__file__)
_EXPECTED = {
    'box_stepper.so': '58ee8c61bffc3d4e18edc9e56a326495b6a218348bbfb13f7a012a946039b0a5',
    'box_extras.so': '0878b5b9d48d71e6bb1a83792776a7f59a529239cc1ca35e9a55102721bde2a6',
    'multi_color_controller.so': 'b7e3bc21156fb9df9f5eea07f2c596a17c7ea5db852a36139ba9773160e43592',
}


def _index(value):
    if type(value) is not int or not 0 <= value < 16:
        raise ValueError('expected an integer index from 0 through 15')
    return value


class RefillToolIdentity:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.config_error = config.error
        self.gcode = self.printer.lookup_object('gcode')
        self.enabled = False
        self.active = None
        self.corrected_count = 0
        self.last_correction = None
        self.last_error = None
        self.printer.register_event_handler('klippy:connect', self._install)

    def _install(self):
        if self.enabled:
            return
        for name, expected in _EXPECTED.items():
            try:
                with open(os.path.join(_FIRMWARE_DIRECTORY, name), 'rb') as stream:
                    actual = hashlib.sha256(stream.read()).hexdigest()
            except OSError as exc:
                raise self.config_error('QIDI refill identity: cannot read %s: %s' % (name, exc))
            if actual != expected:
                raise self.config_error('QIDI refill identity: unsupported %s hash; remove this extension or revalidate it before using updated firmware' % name)
        self.box = self.printer.lookup_object('box_extras')
        entry = self.gcode.mux_commands.get('AUTO_RELOAD_FUNC')
        if not entry or entry[0] != 'SLOT' or not entry[1]:
            raise self.config_error('QIDI refill identity: expected AUTO_RELOAD_FUNC SLOT handlers are missing')
        replacements = {}
        for slot, handler in entry[1].items():
            owner = getattr(handler, '__self__', None)
            if (not isinstance(slot, str) or not slot.startswith('slot')
                    or not slot[4:].isdigit() or not 0 <= int(slot[4:]) < 16
                    or getattr(owner, 'stepper_name', None) != slot
                    or getattr(handler, '__name__', None) != 'cmd_detect_auto_reload_func'):
                raise self.config_error('QIDI refill identity: unexpected AUTO_RELOAD_FUNC handler')
            replacements[slot] = functools.partial(self._run, handler, slot)
        self.original_save = self.box.save_variable
        self.box.save_variable = self._save
        entry[1].update(replacements)
        self.enabled = True
        logging.info('QIDI_REFILL_TOOL_IDENTITY enabled version=%s handlers=%d', VERSION, len(replacements))

    def _reject(self, message):
        self.last_error = message
        logging.error('QIDI_REFILL_TOOL_IDENTITY rejected: %s', message)
        # A failed precondition must not leave a print silently consuming an
        # exhausted donor. PAUSE retains the vendor's normal parking behavior.
        self.gcode.run_script_from_command('PAUSE')
        raise self.gcode.error('QIDI refill identity: ' + message)

    def _run(self, original, donor, gcmd):
        if self.active is not None:
            self._reject('another inlet refill is already active')
        try:
            logical = _index(self.box.get_value_by_key('extrude_state'))
        except ValueError:
            self._reject('active logical tool is invalid')
        if self.box.get_value_by_key('value_t%d' % logical) != donor:
            self._reject('active logical tool does not map to exhausted %s' % donor)
        self.active = {'logical': logical, 'donor': donor}
        try:
            return original(gcmd)
        finally:
            self.active = None

    def _save(self, key, value):
        if key != 'extrude_state' or self.active is None:
            return self.original_save(key, value)
        logical = self.active['logical']
        try:
            physical = _index(value)
        except ValueError:
            self._reject('replacement physical slot is invalid')
        replacement = 'slot%d' % physical
        if replacement == self.active['donor']:
            self._reject('replacement is the exhausted donor')
        if self.box.get_value_by_key('value_t%d' % logical) != replacement:
            self._reject('replacement does not match the updated logical mapping')
        stepper = self.printer.lookup_object('box_stepper ' + replacement, None)
        if stepper is None or stepper.r_endstop_state != 0:
            self._reject('replacement inlet is not present')
        result = self.original_save(key, logical)
        self.corrected_count += 1
        self.last_correction = dict(self.active, replacement=replacement)
        logging.info('QIDI_REFILL_TOOL_IDENTITY preserved logical=T%d donor=%s replacement=%s', logical, self.active['donor'], replacement)
        return result

    def get_status(self, eventtime):
        return {'enabled': self.enabled, 'version': VERSION,
                'active': None if self.active is None else dict(self.active),
                'corrected_count': self.corrected_count,
                'last_correction': self.last_correction, 'last_error': self.last_error}


def load_config(config):
    return RefillToolIdentity(config)
