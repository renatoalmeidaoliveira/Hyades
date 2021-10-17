from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hyades.device.device import Device

from scrapli import Scrapli, AsyncScrapli

class scrapli_wrapper():
    def __init__(self, device: Device):
        self.device = device

        device_data = {
           "host": device.hostname,
           "auth_username": device.username,
           "auth_password": device.password,
           "auth_strict_key": False,
           "platform": device.platform,
        }
        if hasattr(device, 'enable_password'):
            device_data['auth_secondary'] = device.enable_password
        
        scrapli_args = [
            'auth_private_key',
            'auth_private_key_passphrase',
            'auth_strict_key',
            'auth_bypass',
            'timeout_socket',
            'transport',
            'timeout_transport',
            'timeout_ops',
            'comms_prompt_pattern',
            'comms_return_char',
            'ssh_config_file',
            'ssh_known_hosts_file',
            'on_init',
            'on_open',
            'on_close',
            'transport_options',
            'channel_lock',
            'channel_log',
            'channel_log_mode',
            'logging_uid',
            'privilege_levels',
            'default_desired_privilege_level',
            'failed_when_contains',
            'textfsm_platform',
            'genie_platform'
        ]
        for arg in scrapli_args:
            if hasattr(device, arg):
                device_data[arg] = getattr(device, arg)
        
        if device.mode == "async":
            mode = "async"
            self.conn = AsyncScrapli(**device_data)

        else:
            mode = "sync"
            self.conn = Scrapli(**device_data)

        setattr(device, "connected", self.connected)

        methods = ['connect', 'disconnect', 'execute', 'configure']
        for method in methods:
            try:
                setattr(device, method, getattr(self, f"{mode}_{method}"))
            except AttributeError:
                raise Exception(f"Method {method} not Implemented")
        
    @property
    def connected(self):
        return self.conn.isalive()
      
    async def async_connect(self):
        return await self.conn.open()

    async def async_disconnect(self):
        if self.connected:
            await self.conn.close()    

    async def async_execute(self, cmd):
        out = await self.conn.send_command(cmd)
        return out.result
         
    async def async_configure(self, cmd):
        out = await self.conn.send_configs(cmd)
        return out.result

    def sync_connect(self):
        self.conn.open()
    
    def sync_disconnect(self):
        if self.connected:
            self.conn.close()    

    def sync_execute(self, cmd):
        out = self.conn.send_command(cmd)
        return out.result
         
    def sync_configure(self, cmd):
        out = self.conn.send_configs(cmd)
        return out.result
