# coding: utf8
from __future__ import unicode_literals, print_function

import os
import sys
import locale
import textwrap


class MESSAGES(object):
    GOOD = 'good'
    FAIL = 'fail'
    WARN = 'warn'
    INFO = 'info'


COLORS = {
    MESSAGES.GOOD: 2,
    MESSAGES.FAIL: 1,
    MESSAGES.WARN: 3,
    MESSAGES.INFO: 4,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'pink': 5,
    'cyan': 6,
    'white': 7,
    'grey': 8
}

ICONS = {
    MESSAGES.GOOD: '\u2714',
    MESSAGES.FAIL: '\u2718',
    MESSAGES.WARN: '\u26a0',
    MESSAGES.INFO: '\u2139'
}


def color(text, fg=None, bg=None, bold=False):
    """Color text by applying ANSI escape sequence.

    text (unicode): The text to be formatted.
    fg (unicode / int): Foreground color. String name or 0 - 256 (see COLORS).
    bg (unicode / int): Background color. String name or 0 - 256 (see COLORS).
    bold (bool): Format text in bold.
    RETURNS (unicode): The formatted text.
    """
    fg = COLORS.get(fg, fg)
    bg = COLORS.get(bg, bg)
    if not any([fg, bg, bold]):
        return text
    styles = []
    if bold:
        styles.append('1')
    if fg:
        styles.append('38;5;{}'.format(fg))
    if bg:
        styles.append('48;5;{}'.format(bg))
    return '\x1b[{}m{}\x1b[0m'.format(';'.join(styles), text)


def wrap(text, wrap_max=80, indent=4):
    """Wrap text at given width using textwrap module.

    text (unicode): The text to wrap.
    wrap_max (int): Maximum line width, including indentation. Defaults to 80.
    indent (int): Number of spaces used for indentation. Defaults to 4.
    RETURNS (unicode): The wrapped text with line breaks.
    """
    indent = indent * ' '
    wrap_width = wrap_max - len(indent)
    text = to_string(text)
    return textwrap.fill(text, width=wrap_width, initial_indent=indent,
                         subsequent_indent=indent, break_long_words=False,
                         break_on_hyphens=False)


def locale_escape(string, errors='replace'):
    """Mangle non-supported characters, for savages with ASCII terminals.

    string (unicode): The string to escape.
    errors (unicode): The str.encode errors setting. Defaults to `'replace'`.
    RETURNS (unicode): The escaped string.
    """
    encoding = locale.getpreferredencoding()
    string = to_string(string)
    string = string.encode(encoding, errors).decode('utf8')
    return string


def supports_ansi():
    """Returns True if the running system's terminal supports ANSI escape
    sequences for color, formatting etc. and False otherwise. Inspired by
    Django's solution – hacky, but an okay approximation.
    """
    # See: https://stackoverflow.com/q/7445658/6400719
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    if not supported_platform:
        return False
    return True


def to_string(text):
    """Minimal compat helper to make sure text is unicode. Mostly used to
    convert Paths and other Python objects.

    text: The text/object to be converted.
    RETURNS (unicode): The converted string.
    """
    is_python2 = sys.version_info[0] == 2
    if is_python2:
        basestring_ = basestring
    else:
        basestring_ = str
    if not isinstance(text, basestring_):
        if is_python2:
            text = str(text).decode('utf8')
        else:
            text = str(text)
    return text
