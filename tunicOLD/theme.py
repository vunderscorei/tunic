import darkdetect
from types import SimpleNamespace

_LIGHT : SimpleNamespace = SimpleNamespace(
    hyperlink='blue'
)

_DARK : SimpleNamespace = SimpleNamespace(
    hyperlink='cadetblue2'
)

theme : SimpleNamespace = _LIGHT if darkdetect.isLight() else _DARK
