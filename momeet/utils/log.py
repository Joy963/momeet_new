#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import logging.handlers
import sys
import curses

from .escape import to_unicode, unicode_type, basestring_type


def _safe_unicode(s):
    try:
        return to_unicode(s)
    except UnicodeDecodeError:
        return repr(s)


def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


class LogFormatter(logging.Formatter):
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s-->%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y-%m-%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(self, color=True, fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT, colors=DEFAULT_COLORS):
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt
        self._colors = {}
        if color and _stderr_supports_color():
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")

            for levelno, code in colors.items():
                self._colors[levelno] = unicode_type(curses.tparm(fg_color, code), "ascii")
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")
        else:
            self._normal = ''

    def format(self, record):
        try:
            message = record.getMessage()
            assert isinstance(message, basestring_type)
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(_safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def enable_logging(logger, file=''):
    if not file:
        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter())
    else:
        channel = logging.FileHandler(
            filename=file
        )
        channel.setFormatter(LogFormatter(color=False))
    logger.addHandler(channel)

def get_default_logger():
    logger = logging.getLogger("momeet")
    return logger

