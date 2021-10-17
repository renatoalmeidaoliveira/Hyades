from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from hyades.device.device import Device

from hyades.connection.base_wrapper import base_wrapper
from hyades.connection.fabric import ConnectionFabric
from genie.conf.base import Device as genie_device

@ConnectionFabric.register()
class scrapli_wrapper(base_wrapper):
    registry_name: str = 'unicon'

    def configure(self, device: Device) -> Dict[str,str]:
        self.device = device
        self.manager = self
        if device.mode == "async":
            raise UnsuportedMode("Async isn't supported for Unicon")          
        
        device_data = {
           "os": device.platform,
           "credentials": {
               'default' : {
                   'username': device.username,
                   'password': device.password
               },
           },
           'connections': {
               'a': {
                   'protocol': device.transport,
                   "ip": device.hostname,   

               },
           },
        }
        
        self.conn = genie_device(device.name, **device_data)

        mappings = {}
        methods = ['connect', 'disconnect', 'execute', 'configure']
        for method in methods:
            mappings[method] = getattr(self, f"{device.mode}_{method}")
        
        return mappings
        
    @property
    def connected(self):
        return self.conn.connected
      
    def sync_connect(self):
        try:
            log_mode = self.device.log_mode
        except AttributeError:
            log_mode = False
        try:
            learn_mode = self.device.learn_hostname
        except AttributeError:
            learn_mode = True

        self.conn.connect(log_stdout=log_mode, learn_hostname=learn_mode)
    
    def sync_disconnect(self):
        if self.connected:
            self.conn.disconnect()    

    def sync_execute(self, cmd):
        out = self.conn.execute(cmd)
        return out
         
    def sync_configure(self, cmd):
        out = self.conn.configure(cmd)
        return out

class UnsuportedMode(Exception):
    '''
        Raises when try to use async with sync module
    '''