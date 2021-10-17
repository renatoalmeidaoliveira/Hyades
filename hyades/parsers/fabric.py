from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hyades.device.device import Device

from hyades.parsers.default import default_wrapper


class ParserFabric():
    def __init__(self, device: Device):
        self.manager = default_wrapper(device)
        