import meraki

device_output = '''
Latitude: {lat}
Longitude: {lng}
Address: {address}
Serial: {serial}
MAC Address: {mac}
LAN IP Address: {lanIp}
Model: {model}
'''

dashboard = meraki.DashboardAPI()

my_orgs = dashboard.organizations.getOrganizations()
org_id = my_orgs[0]['id']

my_devices = dashboard.organizations.getOrganizationDevices(organizationId=org_id)
print("\nNúmero total de dispositivos: {}".format(len(my_devices)))

for device in my_devices:
    print(device_output.format(
        lat=device.get('lat'),
        lng=device.get('lng'),
        address=device.get('address'),
        serial=device.get('serial'),
        mac=device.get('mac'),
        lanIp=device.get('lanIp'),
        model=device.get('model')
    ))