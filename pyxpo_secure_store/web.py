"""Web backend for `pyxpo build web`: the page's `localStorage`, so values survive a reload.

The browser has no keychain. Values are stored as plain text for this site's origin, readable by any script on the
page, and `requireAuthentication` is not available. Keep only what the page would hold anyway (a session token)."""
from __future__ import annotations

from typing import Any, Dict, List

PREFIX = "pyxpo-secure-store:"


def _storage() -> Any:
    import js  # type: ignore[import-not-found]

    return js.localStorage


def _name(key: str, o: Dict[str, Any]) -> str:
    return PREFIX + str(o.get("keychainService") or "app") + "-" + key


def call(method: str, args: List[Any]) -> Any:
    if method == "canUseBiometric":
        return False
    if method in ("get", "set", "delete"):
        o = dict(args[-1] or {})
        if o.get("requireAuthentication"):
            raise RuntimeError("requireAuthentication is not supported on the web")
        s, name = _storage(), _name(str(args[0]), o)
        if method == "get":
            v = s.getItem(name)
            return None if v is None else str(v)
        if method == "set":
            s.setItem(name, str(args[1]))
        else:
            s.removeItem(name)
        return None
    raise RuntimeError("SecureStore.%s is not available on the web" % method)
