import time

from hyades.inventory.inventory import InventoryManager
inventory = InventoryManager('inventory.yml')

connectors_result = {}

for device in inventory.filter(mode='sync'):
    connector = device.connection_manager.registry_name
    print(f'\nStart collecting {device.name} with {connector}')
    connectors_result[connector] = []
    for it in range(10):
        start = time.time()
        device.connect()
        output = device.parse("show version")
        print(output)
        device.disconnect()
        end = time.time()
        connectors_result[connector].append(end - start)

print('\n\n')
for connector in connectors_result:
    total_time  = sum(connectors_result[connector])
    mean_time = total_time/len(connectors_result[connector])
    min_time = min(connectors_result[connector])
    max_time = max(connectors_result[connector])
    print(f"Connector: {connector}:\n"
          f"Max time: {max_time}\n"
          f"Min time: {min_time}\n"
          f"Mean time: {mean_time}\n\n")
    