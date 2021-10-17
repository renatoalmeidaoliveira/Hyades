import asyncio
import time

from hyades.inventory.inventory import InventoryManager
inventory = InventoryManager('inventory.yml')
async_devices = [device for device in inventory.filter(mode='async')]
sync_devices = [device for device in inventory.filter(mode='sync')]
async_devices_version = {}
async def get_config(dev):
    try:
        print(f'Start collecting {dev.name}')
        await dev.connect()
        output = await dev.parse("show version")
        async_devices_version[dev.name] = output
    except Exception as e:
        print(e)
    finally:
        await dev.disconnect()
        print(f'End collecting {dev.name}')
async def async_main():
    coros = [get_config(dev) for dev in async_devices]
    await asyncio.gather(*coros)
async_start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(async_main())
async_end = time.time()
sync_device_version = {}
sync_start = time.time()
for device in sync_devices:
    print(f'Start collecting {device.name}')
    device.connect()
    output = device.parse("show version")
    sync_device_version[device.name] = output
    device.disconnect()
    print(f'End collecting {device.name}')
sync_end = time.time()
print(f"\n\nAsync Result:\n{async_devices_version}\nTime used: {async_end - async_start}\n\n")
print(f"Sync Result:\n{sync_device_version}\nTime used: {sync_end - sync_start}\n\n")