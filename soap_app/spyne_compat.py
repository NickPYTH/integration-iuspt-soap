"""Compatibility helpers for Spyne 2.14 on Python 3.12+ (including 3.14).

Spyne 2.14 vendors an old ``six`` module whose ``six.moves`` importer no longer
works, and it still uses ``urllib.parse.splittype`` / ``splithost`` which were
removed from the stdlib. This module must be imported before Spyne.
"""

from __future__ import annotations

import http.cookies
import sys
import types
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable, Iterator, MutableSet, Sequence


def _restore_urllib_parse_helpers():
    if not hasattr(urllib.parse, "splittype"):

        def splittype(url):
            if ":" not in url:
                return None, url
            scheme, rest = url.split(":", 1)
            return scheme.lower(), rest

        urllib.parse.splittype = splittype

    if not hasattr(urllib.parse, "splithost"):

        def splithost(url):
            if url.startswith("//"):
                host, sep, path = url[2:].partition("/")
                if sep:
                    path = "/" + path
                return host, path
            return None, url

        urllib.parse.splithost = splithost


def _install_six_moves():
    if "spyne.util.six.moves" in sys.modules:
        return

    collections_abc = types.ModuleType("spyne.util.six.moves.collections_abc")
    collections_abc.MutableSet = MutableSet
    collections_abc.Sequence = Sequence
    collections_abc.Iterable = Iterable
    collections_abc.Iterator = Iterator

    http_cookies = types.ModuleType("spyne.util.six.moves.http_cookies")
    http_cookies.SimpleCookie = http.cookies.SimpleCookie

    urllib_parse = types.ModuleType("spyne.util.six.moves.urllib.parse")
    urllib_parse.unquote = urllib.parse.unquote
    urllib_parse.quote = urllib.parse.quote
    urllib_parse.urlencode = urllib.parse.urlencode
    urllib_parse.splittype = getattr(urllib.parse, "splittype", None)
    urllib_parse.splithost = getattr(urllib.parse, "splithost", None)

    urllib_request = types.ModuleType("spyne.util.six.moves.urllib.request")
    urllib_request.Request = urllib.request.Request
    urllib_request.urlopen = urllib.request.urlopen

    urllib_error = types.ModuleType("spyne.util.six.moves.urllib.error")
    urllib_error.HTTPError = urllib.error.HTTPError

    urllib_mod = types.ModuleType("spyne.util.six.moves.urllib")
    urllib_mod.parse = urllib_parse
    urllib_mod.request = urllib_request
    urllib_mod.error = urllib_error

    moves = types.ModuleType("spyne.util.six.moves")
    moves.collections_abc = collections_abc
    moves.http_cookies = http_cookies
    moves.urllib = urllib_mod

    sys.modules["spyne.util.six.moves"] = moves
    sys.modules["spyne.util.six.moves.collections_abc"] = collections_abc
    sys.modules["spyne.util.six.moves.http_cookies"] = http_cookies
    sys.modules["spyne.util.six.moves.urllib"] = urllib_mod
    sys.modules["spyne.util.six.moves.urllib.parse"] = urllib_parse
    sys.modules["spyne.util.six.moves.urllib.request"] = urllib_request
    sys.modules["spyne.util.six.moves.urllib.error"] = urllib_error


_restore_urllib_parse_helpers()
_install_six_moves()
