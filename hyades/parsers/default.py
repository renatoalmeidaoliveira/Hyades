from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from hyades.device.device import Device

from genie.conf.base import Device as genie_device

import asyncio

class default_wrapper():
    def __init__(self, device: Device) -> None:
        self.device = device
        if device.mode == "async":
            mode = "async"
        else:
            mode = "sync"
        
        platform_translation = {
            "hp_comware": 'comware',
            'cisco_iosxe': 'iosxe',
            'cisco_iosxr': 'iosxr',
            'cisco_nxos': 'nxos',
            'juniper_junos': 'junos',
        }
        if device.platform in platform_translation:
            platform = platform_translation[device.platform]
        else:
            platform = device.platform
        
        self.genie_device = genie_device(device.name,
                                         custom={"abstraction": {"order": ["os"]}},
                                         os=platform)
        setattr(device, 'parse', getattr(self, f"{mode}_parse"))
        
    def sync_parse(self, command: str) -> Dict:
        output = {}
        cmd_output = self.device.execute(command)
        output = self.genie_device.parse(command, output=cmd_output)
        return output
    
    async def async_parse(self, command: str) -> Dict:
        output = {}
        cmd_output = await self.device.execute(command)
        output = self.genie_device.parse(command, output=cmd_output)
        return output

class Unconnected(Exception):
    '''
        Raises when try to execute on unconnected Devices
    '''