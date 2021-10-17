from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hyades.device.device import Device
    
from hyades.connection.scrapli_wrapper import scrapli_wrapper



class ConnectionFabric():
    def __init__(self, device: Device):
        manager = device.connection_manager
        registred = {
            'scrapli' : scrapli_wrapper
        }

        if manager in registred:
            manager_cls = registred[manager]
            self.manager = manager_cls(device)
